#[path = "../../measurement.rs"]
mod measurement;

use std::{mem::size_of, time::Instant};

use bolt_rs::{
    BinaryElem, BinaryElem32 as B32, BinaryElem128 as B128, ColMajorMatrix, ReedSolomonEncoding,
    brakedown::{BrakedownEncoder, BrakedownParams}, expander::ExpanderMatrix,
    raa::{raa_encode, random_permutation}, sketch_code::encode_poly_matrix_rs_with_params,
};
use rand::{RngExt, SeedableRng, rngs::StdRng};

fn input<F: BinaryElem>(n: usize) -> Vec<F> {
    let mut rng = StdRng::seed_from_u64(112);
    (0..n).map(|_| F::from_u128(rng.random())).collect()
}

// The helper maintains a single buffer and restores input outside the timer.
fn encode_buffer<F: BinaryElem>(
    msg: &[F],
    len: usize,
    setup: f64,
    zero_tail: bool,
    mut encode: impl FnMut(&mut ColMajorMatrix<F>),
) {
    let buffer = std::cell::RefCell::new(Some(ColMajorMatrix::zeros(1, len)));
    println!("GEOMETRY {} {len} {}", msg.len(), msg.len()*size_of::<F>());
    measurement::measure(setup, len, || {
        let mut m = buffer.borrow_mut().take().unwrap();
        m.as_mut_slice()[..msg.len()].copy_from_slice(msg);
        if zero_tail {
            m.as_mut_slice()[msg.len()..].fill(F::zero());
        }
        m
    }, |mut word| {
        encode(&mut word);
        word
    }, |word| {
        let v = word.as_slice();
        let check = (v.len(), v.iter().any(|&x| x != F::zero()));
        buffer.replace(Some(word));
        check
    });
}

fn raa<F: BinaryElem + Send + Sync>(n: usize, c: usize) {
    let length = n*c;
    let msg = input::<F>(n);
    let start = Instant::now();
    let mut rng = StdRng::seed_from_u64(113);
    let p1 = random_permutation(length, &mut rng);
    let p2 = random_permutation(length, &mut rng);
    let mut temp = ColMajorMatrix::zeros(1, length);
    encode_buffer(&msg, length, measurement::ms(start), false, |word| {
        raa_encode(word, &mut temp, n, c, &p1, &p2);
    });
}

fn main() {
    let args: Vec<_> = std::env::args().skip(1).collect();
    let [mode, field, k, c] = args.as_slice() else { panic!("encoder field log_k rate"); };
    let n = 1 << k.parse::<usize>().unwrap();
    if mode == "raa" {
        let c: usize = c.parse().unwrap();
        return match field.as_str() {
            "bf32" => raa::<B32>(n, c),
            "bf128" => raa::<B128>(n, c),
            _ => panic!("unknown field"),
        };
    }
    assert_eq!(field, "bf32");
    let msg = input::<B32>(n);
    let start = Instant::now();
    match mode.as_str() {
        "rs" => {
            let length = n*c.parse::<usize>().unwrap();
            let rs = ReedSolomonEncoding::<B32>::new(n, length);
            encode_buffer(&msg, length, measurement::ms(start), true, |word| {
                rs.encode_non_systematic(word.as_mut_slice());
            });
        }
        "bolt-xor" | "bolt32" => {
            let c = c.parse::<usize>().unwrap();
            let expander = if mode == "bolt-xor" {
                ExpanderMatrix::<B32>::new_gallager_binary_with_seed(n, 8, 64, 113).unwrap()
            } else {
                ExpanderMatrix::<B32>::new_with_seed(n, 8, 64, 113)
            };
            let check_len = expander.num_constraints();
            assert_eq!(check_len, n/8);
            let rs = ReedSolomonEncoding::new(check_len, check_len*c);
            let length = n+check_len*c;
            let setup = measurement::ms(start);
            println!("PARAM expander_left_degree=8 expander_right_degree=64 inner_inverse_rate={c}");
            encode_buffer(&msg, length, setup, false, |word| {
                if mode == "bolt-xor" {
                    expander.encode_matrix_xor_only(word);
                } else {
                    expander.encode_matrix_inner_product_deferred_32(word);
                }
                encode_poly_matrix_rs_with_params(word, n, check_len, &rs);
            });
        }
        "brakedown" => {
            let (alpha, inverse, cn, dn) = match c.as_str() {
                "native-high" => (0.238, 1.0/0.674, 13, 14),
                "native-low" => (0.238, 1.0/0.506, 13, 14),
                c => (0.238, c.parse::<f64>().unwrap(), 13, 14),
            };
            let brakedown = BrakedownEncoder::new_with_rng(
                BrakedownParams { alpha, r: inverse, c: cn, d: dn, n0: 64 },
                n, &mut StdRng::seed_from_u64(113)
            );
            let setup = measurement::ms(start);
            println!("PARAM alpha={alpha} c_n={cn} d_n={dn} base_limit=64");
            encode_buffer(&msg, brakedown.codeword_len(), setup, false, |word| brakedown.encode(word));
        }
        _ => panic!("unknown encoder"),
    }
}
