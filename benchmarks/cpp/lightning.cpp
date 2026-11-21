#include "measurement.hpp"
#include <bit>
#include <limits>

#define main lightning_reference_main
#include "../source/lightning/lightning.cpp"
#undef main

// The native branch recurses while n >= BASE_N and pads the terminal RS to a
// power of two. Predict its length so rate selection needs no graph allocation.
int predicted_parity_length(int n) {
    if (n < BrakedownCode::BASE_N) {
        auto min_n = static_cast<unsigned>(std::ceil((double)n / (1.0 / BrakedownCode::R_PAR)));
        return static_cast<int>(std::bit_ceil(min_n));
    }
    auto an = std::max(1, (int)std::round(BrakedownCode::ALPHA * n));
    auto arn = std::max(1, (int)std::round(BrakedownCode::ALPHA * BrakedownCode::R_PAR * n));
    auto tail = std::max(1, (int)std::round((BrakedownCode::R_PAR - 1.0 - BrakedownCode::R_PAR * BrakedownCode::ALPHA) * n));
    return n + std::max(arn, predicted_parity_length(an)) + tail;
}

int half_rate_sketch(int n) {
    int lo = 1;
    int hi = n;
    while (lo < hi) {
        const int mid = lo + (hi - lo)/2;
        if (predicted_parity_length(mid) < n)
            lo = mid + 1;
        else
            hi = mid;
    }
    if (lo > 1 && n - predicted_parity_length(lo - 1) < predicted_parity_length(lo) - n)
        return lo - 1;
    return lo;
}

int main(int argc, char** argv) {
    if (argc != 5) {
        std::cerr << "expected operation field log_k rate\n";
        return 2;
    }
    int n = 1 << std::stoi(argv[3]);
    const std::string mode = argv[4];
    Params params = table.at(mode == "native-high" ? 0.003 : 0.006);
    int right = mode == "half" ? half_rate_sketch(n) : (int)std::ceil(params.alpha * n);
    initPairing(mcl::BN_SNARK1);
    mt19937_64 rng(112);
    std::vector<uint64_t> msg(n);
    for (auto& x : msg) x = rng() % 10000000001ULL;
    const auto start = BenchClock::now();
    BrakedownCode inner;
    mt19937_64 rng_bd(54321);
    inner.setup(right, rng_bd);
    const auto parity_len = inner.codeword_len();
    if (parity_len != predicted_parity_length(right))
        throw std::runtime_error("Lightning codeword geometry mismatch");
    Random_matrix sketch(n, right, params.degree, 1);
    const auto setup = bench_ms(start);
    std::vector<F> compressed(right, F(0)), parity(parity_len, F(0));
    const auto code_len = std::size_t(n) + parity_len;
    std::cout << "GEOMETRY " << n << ' ' << code_len << ' ' << msg.size() * sizeof(uint64_t) << '\n';
    std::cout << "PARAM input_storage=u64 output_parity_storage=" << sizeof(F)
              << " actual_sketch_fraction=" << double(right)/n << " degree=" << params.degree << '\n';
    int written = 0;
    measure(setup, code_len, [&] {
        sketch.aggregate_batch_left_major(msg.data(), compressed.data());
        written = inner.encode(compressed.data(), parity.data());
    }, [&] {
        return written == parity_len && std::any_of(parity.begin(), parity.end(), [](const F& x){ return !x.isZero(); });
    });
}
