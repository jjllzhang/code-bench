#[path = "../../measurement.rs"]
mod measurement;

use std::{mem::size_of, time::Instant};
use ff::Field;
use lcpc_brakedown_pc::{
    codespec::{SdigCode2, SdigCode3, SdigSpecification},
    encode::encode,
    matgen::generate,
};
use lcpc_test_fields::ft127::Ft127;
use rand::{SeedableRng, rngs::StdRng};

fn run<S: SdigSpecification>(k: usize) {
    let n = 1 << k;
    let mut rng = StdRng::seed_from_u64(112);
    let msg: Vec<Ft127> = (0..n).map(|_| Ft127::random(&mut rng)).collect();
    let start = Instant::now();
    let (pre, post) = generate::<Ft127, S>(n, 113);
    let length = n + post.last().unwrap().cols()
        + pre[..pre.len()-1].iter().map(|pc| pc.rows()).sum::<usize>()
        + post.iter().map(|pc| pc.rows()).sum::<usize>();
    let setup = measurement::ms(start);
    let buffer = std::cell::RefCell::new(Some(vec![Ft127::zero(); length]));
    println!("GEOMETRY {n} {length} {}",n*size_of::<Ft127>());
    measurement::measure(setup, length, || {
        let mut word = buffer.borrow_mut().take().unwrap();
        word[..n].copy_from_slice(&msg);
        word
    }, |mut word| {
        encode(&mut word, &pre, &post);
        word
    }, |word| {
        let check = (word.len(),word.iter().any(|x| *x != Ft127::zero()));
        buffer.replace(Some(word));
        check
    });
}

fn main() {
    let args: Vec<_> = std::env::args().skip(1).collect();
    let [kind, field, k, _rate] = args.as_slice() else { panic!("kind field k rate"); };
    assert_eq!(field, "ft127");
    let k = k.parse().unwrap();
    match kind.as_str() {
        "sdig2" => run::<SdigCode2>(k),
        "sdig3" => run::<SdigCode3>(k),
        _ => panic!("unknown family"),
    }
}
