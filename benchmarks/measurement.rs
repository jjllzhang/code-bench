use std::{hint::black_box, mem::MaybeUninit, time::Instant};

pub fn ms(start: Instant) -> f64 {
    start.elapsed().as_secs_f64() * 1000.0
}

fn faults() -> (i64, i64) {
    let mut usage = MaybeUninit::<libc::rusage>::uninit();
    assert_eq!(unsafe { libc::getrusage(libc::RUSAGE_SELF, usage.as_mut_ptr()) }, 0);
    let usage = unsafe { usage.assume_init() };
    (usage.ru_minflt, usage.ru_majflt)
}

pub fn measure<I, O>(
    setup_ms: f64,
    expected: usize,
    mut prepare: impl FnMut() -> I,
    mut encode: impl FnMut(I) -> O,
    mut check: impl FnMut(O) -> (usize, bool),
) {
    println!("SETUP {setup_ms:.9}");
    for i in 0..4 {
        let input = prepare();
        let before = faults();
        let start = Instant::now();
        let output = black_box(encode(black_box(input)));
        let elapsed = ms(start);
        let after = faults();
        let (len, nonzero) = check(output);
        assert_eq!(len, expected);
        assert!(nonzero);
        println!("ITER {i} {elapsed:.9} {len} {} {}", after.0 - before.0, after.1 - before.1);
    }
}

pub fn vector<T: Copy + PartialEq>(
    setup_ms: f64,
    expected: usize,
    zero: T,
    encode: impl FnMut(()) -> Vec<T>,
) {
    measure(setup_ms, expected, || (), encode, |v| {
        (v.len(), v.iter().any(|&x| x != zero))
    });
}
