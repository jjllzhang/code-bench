#include "measurement.hpp"
#include <algorithm>
#include <cstdint>
#include <random>
#include <span>
#include <string>
#include <spin/Code.h>

int main(int argc, char** argv) {
    if (argc != 5) {
        std::cerr << "expected operation field log_k inverse_rate\n";
        return 2;
    }
    const std::size_t n = std::size_t{1} << std::stoul(argv[3]);
    auto kind = std::string(argv[1]) == "imt" ? spin::Parameters::T128S19 : spin::Parameters::PacketRs8T64;
    if (!spin::valid_message_size(kind, n)) {
        std::cerr << "domain limit from spin::valid_message_size\n";
        return 3;
    }
    const auto start = BenchClock::now();
    spin::Code code({n, kind, 17, 43});
    auto ws = code.make_workspace(spin::Width::Bits128);
    const auto setup = bench_ms(start);
    if (code.message_size() != n || code.code_size() != 2*n || !code.supports_forward(spin::Width::Bits128))
        throw std::runtime_error("unexpected SPIN dimensions or backend");
    spin::Buffer input(n * 16), output(code.code_size() * 16);
    std::mt19937_64 rng(112);
    for (auto& x : input.bytes())
        x = std::byte(rng() & 255);
    std::fill(output.bytes().begin(), output.bytes().end(), std::byte{0});
    std::cout << "GEOMETRY " << n << ' ' << code.code_size() << ' ' << input.bytes().size() << '\n';
    measure(setup, code.code_size(), [&] {
        code.forward_bytes(input.bytes(), output.bytes(), ws, spin::OutputStores::Cached);
    }, [&] {
        auto cw = output.bytes();
        return std::any_of(cw.begin(), cw.end(), [](std::byte x){return x != std::byte{0};});
    });
}
