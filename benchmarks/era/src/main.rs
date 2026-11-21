#[path = "../../measurement.rs"]
mod measurement;

use std::{hint::black_box, mem::size_of, time::Instant};

use era_codes::{
    BasefoldCode, BasefoldParams, BrakedownCode, BrakedownParams, EaCode, EaParams, EraCode,
    ErrorCorrectingCode, FieldElement, goldilocks_interleaved, random_permutation,
};
use rand::{SeedableRng, rngs::SmallRng};
use rayon::prelude::*;

fn check_linearity<F: FieldElement>(input: &[F], encode: impl Fn(&[F]) -> Vec<F>) {
    let second: Vec<_> = (0..input.len()).map(|i| F::from_u32(i as u32)).collect();
    let sum: Vec<_> = input.iter().zip(&second).map(|(&a, &b)| a + b).collect();
    let actual = encode(&sum);
    let expected: Vec<_> = encode(input).into_iter().zip(encode(&second)).map(|(a,b)| a+b).collect();
    assert_eq!(actual, expected);
}

fn run<F: FieldElement>(code: &str, k: usize, inv_rate: usize) {
    let n = 1 << k;
    let mut input_rng = SmallRng::seed_from_u64(112);
    let input: Vec<F> = (0..n).map(|_| F::random(&mut input_rng)).collect();
    let mut rng = SmallRng::seed_from_u64(113);
    let start = Instant::now();
    match code {
        "ea" => {
            let encoder = EaCode::new(n, EaParams { inverse_rate: inv_rate, prob_multiplier: 18 }, &mut rng);
            let setup = measurement::ms(start);
            if k <= 10 { check_linearity(&input, |x| encoder.encode(x)); }
            println!("GEOMETRY {n} {} {}", n*inv_rate, n*size_of::<F>());
            measurement::vector(setup, n*inv_rate, F::ZERO, |_| encoder.encode(&input));
        }
        "brakedown" => {
            let encoder = BrakedownCode::new(n, BrakedownParams {
                alpha: 0.3, inverse_rate: inv_rate as f64, cn: 14, dn: 28,
            }, &mut rng);
            let setup = measurement::ms(start);
            let length = encoder.codeword_length();
            if k <= 10 { check_linearity(&input, |x| encoder.encode(x)); }
            println!("PARAM alpha=0.3 c_n=14 d_n=28");
            println!("GEOMETRY {n} {length} {}", n*size_of::<F>());
            measurement::vector(setup, length, F::ZERO, |_| encoder.encode(&input));
        }
        "basefold" => {
            let encoder = BasefoldCode::new(n, BasefoldParams { log_rate: inv_rate.ilog2() as usize }, &mut rng);
            let setup = measurement::ms(start);
            let length = encoder.codeword_length();
            println!("PARAM terminal=repetition");
            println!("GEOMETRY {n} {length} {}", n*size_of::<F>());
            measurement::vector(setup, length, F::ZERO, |_| encoder.encode(&input));
        }
        "era" => {
            let base = BrakedownCode::new(n, goldilocks_interleaved::PARAMS, &mut rng);
            let length = base.block_length()*inv_rate;
            let p1 = random_permutation(&mut rng, length);
            let p2 = random_permutation(&mut rng, length);
            let mut field_vector = || (0..length).map(|_| {
                let mut x = F::random(&mut rng);
                while x.is_zero() {
                    x = F::random(&mut rng);
                }
                x
            }).collect();
            let m1 = field_vector();
            let m2 = field_vector();
            let encoder = EraCode::new(base, inv_rate, p1, p2, m1, m2);
            let setup = measurement::ms(start);
            println!("PARAM alpha=0.04 inner_inverse_rate=1.05 c_n=8 d_n=64 repetition={inv_rate}");
            println!("GEOMETRY {n} {length} {}", n*size_of::<F>());
            measurement::vector(setup, length, F::ZERO, |_| encoder.encode_era(&input));
        }
        "raa" => {
            let length = n*inv_rate;
            let p1 = random_permutation(&mut rng, length);
            let p2 = random_permutation(&mut rng, length);
            let mut first = vec![F::ZERO; length];
            let mut second = vec![F::ZERO; length];
            let setup = measurement::ms(start);
            println!("GEOMETRY {n} {length} {}", n*size_of::<F>());
            measurement::measure(setup, length, || (), |_| {
                // Equivalent to materializing repetition and then gathering pi1.
                first.par_iter_mut().zip(&p1).for_each(|(out, &i)| *out = input[i % n]);
                accumulate(&mut first);
                second.par_iter_mut().zip(&p2).for_each(|(out, &i)| *out = first[i]);
                accumulate(&mut second);
                black_box(&second);
                (second.len(), second[0])
            }, |(len, first)| (len, !first.is_zero()));
        }
        _ => panic!("unknown operation"),
    }
}

fn accumulate<F: FieldElement>(word: &mut [F]) {
    let mut sum = F::ZERO;
    for x in word {
        sum += *x;
        *x = sum;
    }
}

fn main() {
    let args: Vec<_> = std::env::args().skip(1).collect();
    let [name, field, k, c] = args.as_slice() else {
        panic!("encoder field log_k inverse_rate");
    };
    let (k, c) = (k.parse().unwrap(), c.parse().unwrap());
    match field.as_str() {
        "goldilocks" => run::<goldilocks_interleaved::Base>(name, k, c),
        "secp256k1" => run::<ark_secp256k1::Fr>(name, k, c),
        _ => panic!("unknown field"),
    }
}
