#pragma once
#include <chrono>
#include <iomanip>
#include <iostream>
#include <stdexcept>
#include <sys/resource.h>

using BenchClock = std::chrono::steady_clock;

double bench_ms(BenchClock::time_point start) {
    return std::chrono::duration<double, std::milli>(BenchClock::now() - start).count();
}

template<class Encode, class Check>
void measure(double setup_ms, std::size_t length, Encode encode, Check check) {
    std::cout << std::fixed << std::setprecision(9) << "SETUP " << setup_ms << '\n';
    for (unsigned i = 0; i < 4; ++i) {
        rusage before{}, after{};
        getrusage(RUSAGE_SELF, &before);
        auto start = BenchClock::now();
        encode();
        const auto elapsed = bench_ms(start);
        getrusage(RUSAGE_SELF, &after);
        if (!check())
            throw std::runtime_error("encoder returned empty or invalid codeword");
        std::cout << "ITER " << i << ' ' << elapsed << ' ' << length << ' '
                  << after.ru_minflt - before.ru_minflt << ' ' << after.ru_majflt - before.ru_majflt << '\n';
    }
}
