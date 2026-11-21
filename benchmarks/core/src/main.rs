#[path = "../../measurement.rs"]
mod measurement;

use std::{mem::size_of, time::Instant};

use binary_hyperfold::{
    code::{HyperFoldableCode, native::{NativeCode, NativeField}},
    parameters::{HyperFoldConfig as BinaryConfig, HyperFoldParams},
};
use hyperfold_pcs::{
    base_code::BaseCodeImpl, encoder::encode_top, field_m127::Mersenne127,
    matrix_h::LocalMatrix, params::{BaseCodeKind, DiagonalTables, HyperFoldConfig},
    sampling::SampleBase,
};
use p3_baby_bear::BabyBear;
use p3_binary_dft::{AdditiveNtt, AdditiveRsEncoder, ButterflyField, LchNtt, PolyBasisNtt};
use p3_binary_field::{BinaryField16 as B16, BinaryField32 as B32, BinaryField64 as B64, BinaryField128 as B128, TowerLevel};
use p3_binary_qa::{QaEncoder, QaField};
use p3_commit::Encoder;
use p3_dft::{Radix2DitParallel, TwoAdicSubgroupDft};
use p3_field::{ExtensionField, Field, PackedValue, PrimeCharacteristicRing, TwoAdicField};
use p3_goldilocks::Goldilocks as Gold;
use p3_matrix::dense::{RowMajorMatrix, RowMajorMatrixView};
use rand::{RngExt, SeedableRng, rngs::SmallRng};
use rayon::prelude::*;

fn binary_vec<F: TowerLevel>(n: usize, seed: u64) -> Vec<F> {
    let mut rng = SmallRng::seed_from_u64(seed);
    (0..n).map(|_| F::from_le_byte_iter(rng.random::<u128>().to_le_bytes().into_iter())).collect()
}

fn prime_vec<F: PrimeCharacteristicRing>(n: usize, seed: u64) -> Vec<F> {
    let mut rng = SmallRng::seed_from_u64(seed);
    (0..n).map(|_| F::from_u64(rng.random::<u64>())).collect()
}

fn header<F>(k: usize, n: usize) {
    println!("GEOMETRY {} {n} {}", 1usize << k, (1usize << k) * size_of::<F>());
}

fn rs_prime<F: TwoAdicField + Ord>(k: usize, c: usize) {
    let kl = 1 << k;
    let n = kl * c;
    let message = prime_vec::<F>(kl, 112);
    let start = Instant::now();
    let fft = Radix2DitParallel::<F>::default();
    let shift = F::GENERATOR;
    let bits = c.ilog2() as usize;
    fft.prepare_coset_lde(k, bits, shift);
    let setup = measurement::ms(start);
    header::<F>(k, n);
    // The upstream kernel keeps this output allocation. Keep it resident across trials.
    use std::cell::RefCell;
    let reusable = RefCell::new(Some(vec![F::ZERO; n]));
    measurement::measure(
        setup, n,
        || {
            let mut v = reusable.borrow_mut().take().unwrap();
            v.resize(kl, F::ZERO);
            v.copy_from_slice(&message);
            RowMajorMatrix::new(v, 1)
        },
        |m| fft.coset_lde_batch(m, bits, shift),
        |out| {
            let v = out.inner.values;
            let result = (v.len(), v.iter().any(|&x| x != F::ZERO));
            reusable.replace(Some(v));
            result
        },
    );
}

fn rs_binary<F, Ntt>(k: usize, c: usize, ntt: Ntt)
where
    F: ButterflyField,
    Ntt: AdditiveNtt<F> + Sync,
    AdditiveRsEncoder<F, Ntt>: Encoder<F>,
{
    let kl = 1 << k;
    let n = kl * c;
    let message = binary_vec::<F>(kl, 112);
    let start = Instant::now();
    let encoder = AdditiveRsEncoder::new(ntt);
    let setup = measurement::ms(start);
    let view = RowMajorMatrixView::new(message.as_slice(), 1);
    header::<F>(k, n);
    measurement::vector(setup, n, F::ZERO, |_| {
        encoder.encode_batch_borrowed(view, c.ilog2() as usize).values
    });
}

fn butterfly<F: Field>(lo: &mut [F], hi: &mut [F]) {
    let (lo_pack, lo_tail) = F::Packing::pack_slice_with_suffix_mut(lo);
    let (hi_pack, hi_tail) = F::Packing::pack_slice_with_suffix_mut(hi);
    for (u, v) in lo_pack.iter_mut().zip(hi_pack) {
        let (a, b) = (*u, *v);
        (*u, *v) = (a + b, a - b);
    }
    for (u, v) in lo_tail.iter_mut().zip(hi_tail) {
        let (a, b) = (*u, *v);
        (*u, *v) = (a + b, a - b);
    }
}

fn wht<F: Field>(values: &mut [F], depth: usize) {
    // Fuse the many small, cache-local stages. Split each late butterfly into
    // disjoint slices, preserving parallel work even at the largest stage.
    let first = (1 << depth).min(4096);
    values.par_chunks_exact_mut(first).for_each(hyperfold_pcs::base_code::wht_in_place);
    let mut half = first;
    while half < values.len() {
        values.par_chunks_exact_mut(half * 2).for_each(|chunk| {
            let (lo, hi) = chunk.split_at_mut(half);
            lo.par_chunks_exact_mut(4096).zip(hi.par_chunks_exact_mut(4096))
                .for_each(|(a, b)| butterfly(a, b));
        });
        half *= 2;
    }
}

fn qa_prime<F: Field>(k: usize, c: usize) {
    let kl = 1 << k;
    let n = kl * c;
    let message = prime_vec::<F>(kl, 112);
    let start = Instant::now();
    let scale = F::from_usize(kl).inverse();
    let spectra: Vec<_> = prime_vec::<F>(kl * (c - 1), 113).into_iter()
        .map(|x| if x == F::ZERO { scale } else { x * scale }).collect();
    let mut spectrum = vec![F::ZERO; kl];
    let mut out = vec![F::ZERO; n];
    let setup = measurement::ms(start);
    header::<F>(k, n);
    let encode = |spec: &mut [F], word: &mut [F]| {
        spec.copy_from_slice(&message);
        wht(spec, k);
        word[..kl].copy_from_slice(&message);
        for (parity, multiplier) in word[kl..].chunks_exact_mut(kl).zip(spectra.chunks_exact(kl)) {
            parity.par_iter_mut().zip(spec.par_iter()).zip(multiplier.par_iter())
                .for_each(|((dst, &x), &t)| *dst = x * t);
            wht(parity, k);
        }
    };
    if k <= 14 {
        encode(&mut spectrum, &mut out);
        let mut reference = message.clone();
        hyperfold_pcs::base_code::wht_in_place(&mut reference);
        for (i, mult) in spectra.chunks_exact(kl).enumerate() {
            let mut tail: Vec<_> = reference.iter().zip(mult).map(|(&x, &t)| x * t).collect();
            hyperfold_pcs::base_code::wht_in_place(&mut tail);
            assert_eq!(&tail, &out[(i+1)*kl..(i+2)*kl]);
        }
    }
    measurement::measure(setup, n, || (), |_| {
        encode(&mut spectrum, &mut out);
        std::hint::black_box(&out);
        (out.len(), out[0])
    }, |out| (out.0, out.1 != F::ZERO));
}

fn qa_binary<F, S>(k: usize, c: usize)
where F: QaField + ExtensionField<S>, S: QaField
{
    let kl = 1 << k;
    let n = kl * c;
    let msg = binary_vec::<S>(kl, 112);
    let start = Instant::now();
    let spectra = binary_vec::<F>(kl * (c - 1), 113);
    let encoder = QaEncoder::<F>::new(k, c.ilog2() as usize, spectra);
    let setup = measurement::ms(start);
    header::<S>(k, n);
    measurement::vector(setup, n, F::ZERO, |_| encoder.subfield_encode_batch(&msg, 0));
}

fn hf_prime<F: SampleBase>(k: usize, c: usize, r: usize, base: &str) {
    let backend = match base {
        "qa" => BaseCodeKind::Qa,
        "rs" => BaseCodeKind::Rs,
        _ => panic!("unknown base"),
    };
    let config = if k >= 20 {
        HyperFoldConfig::experiment(F::KIND, backend, k, r, c).unwrap()
    } else {
        let m = (4..=8).find(|m| (k-m) % r.ilog2() as usize == 0).unwrap();
        HyperFoldConfig::testing(F::KIND, backend, k, m, r, c, if size_of::<F>() == 8 {3} else {2}).unwrap()
    };
    let message = prime_vec::<F>(1 << k, 112);
    let start = Instant::now();
    let seed = [112; 32];
    let base = BaseCodeImpl::<F>::new(config, &seed).unwrap();
    let diagonals = DiagonalTables::<F>::new(config, &seed);
    let matrix = LocalMatrix::<F>::new(r);
    let setup = measurement::ms(start);
    println!("PARAM mu0={}", config.mu0);
    header::<F>(k, c << k);
    measurement::vector(setup, c << k, F::ZERO, |_| {
        encode_top(config, &base, &matrix, &diagonals, &message, config.depth()).values
    });
}

fn binary_config(k: usize, c: usize, r: usize, bits: usize) -> BinaryConfig {
    // Encoding uses only the code geometry. Keep the default admissible mu0 rule
    // independently of whether the interactive parameter search has a budget.
    let nu = r.ilog2() as usize;
    let mu0 = (4usize..=10).filter(|&m| m + nu <= k && (k - m) % nu == 0)
        .min_by_key(|&m| (m.abs_diff(8), m)).unwrap();
    let d = (k - mu0) / nu;
    let ks: Vec<_> = (0..=d).map(|i| 1 << (mu0+i*nu)).collect();
    let ns = ks.iter().map(|x| x * c).collect();
    BinaryConfig {
        params: HyperFoldParams { mu: k, r, c, base_field_bits: bits, mu_0: Some(mu0), ..Default::default() },
        nu, mu_0: mu0, d, k: ks, n: ns, thresholds: vec![], dual_thresholds: vec![],
        distance: 0., epsilon_code: 0., eta: 0., delta: 0., list_size: 0, queries: 0, epsilon_field: 0.,
    }
}

fn hf_binary_native<F: NativeField>(k: usize, c: usize, r: usize) where B128: ExtensionField<F> {
    let config = binary_config(k, c, r, F::BITS);
    let message = binary_vec::<F>(1 << k, 112);
    let start = Instant::now();
    let native = NativeCode::<F>::setup(&config, &mut SmallRng::seed_from_u64(113));
    let setup = measurement::ms(start);
    println!("PARAM mu0={}", config.mu_0);
    header::<F>(k, c << k);
    measurement::vector(setup, c << k, F::ZERO, |_| native.encode(config.d, &message).values);
}

fn hf_binary_128(k: usize, c: usize, r: usize) {
    let config = binary_config(k, c, r, 128);
    let message = binary_vec::<B128>(1 << k, 112);
    let start = Instant::now();
    let code = HyperFoldableCode::setup(&config, &mut SmallRng::seed_from_u64(113));
    let setup = measurement::ms(start);
    println!("PARAM mu0={}", config.mu_0);
    header::<B128>(k, c << k);
    measurement::vector(setup, c << k, B128::ZERO, |_| code.encode(config.d, &message).values);
}

fn main() {
    let args: Vec<_> = std::env::args().skip(1).collect();
    let [name, field, k, c, extras @ ..] = args.as_slice() else { panic!("name field log_k inverse_rate [arity base]") };
    let (k, c) = (k.parse().unwrap(), c.parse().unwrap());
    let r = || extras[0].parse().unwrap();
    match (name.as_str(), field.as_str()) {
        ("rs", "goldilocks") => rs_prime::<Gold>(k, c),
        ("rs", "babybear") => rs_prime::<BabyBear>(k, c),
        ("lch", "bf32") => rs_binary::<B32, _>(k, c, LchNtt::<B32>::default()),
        ("lch", "bf64") => rs_binary::<B64, _>(k, c, LchNtt::<B64>::default()),
        ("lch", "bf128") => rs_binary::<B128, _>(k, c, LchNtt::<B128>::default()),
        ("poly", "bf128") => rs_binary::<B128, _>(k, c, PolyBasisNtt),
        ("qa", "goldilocks") => qa_prime::<Gold>(k, c),
        ("qa", "m127") => qa_prime::<Mersenne127>(k, c),
        ("qa", "bf32") => qa_binary::<B32, B32>(k, c),
        ("qa", "bf64") => qa_binary::<B64, B64>(k, c),
        ("qa", "bf128") => qa_binary::<B128, B128>(k, c),
        ("qa", "bf32-bf64") => qa_binary::<B64, B32>(k, c),
        ("qa", "bf32-bf128") => qa_binary::<B128, B32>(k, c),
        ("qa", "bf64-bf128") => qa_binary::<B128, B64>(k, c),
        ("hyperfold", "goldilocks") => hf_prime::<Gold>(k, c, r(), &extras[1]),
        ("hyperfold", "m127") => hf_prime::<Mersenne127>(k, c, r(), &extras[1]),
        ("hyperfold", "bf16") => hf_binary_native::<B16>(k, c, r()),
        ("hyperfold", "bf32") => hf_binary_native::<B32>(k, c, r()),
        ("hyperfold", "bf64") => hf_binary_native::<B64>(k, c, r()),
        ("hyperfold", "bf128") => hf_binary_128(k, c, r()),
        _ => panic!("unsupported encoder {name}/{field}"),
    }
}
