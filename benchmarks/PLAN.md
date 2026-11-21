# Code-based PCS 编码器纯编码时间 Benchmark 规划 (`impl-plan-code-encoding-bench`)

- **状态**：v1.2 FINAL（已合并 Jal1n 卡片确认 `msg=45aff629` 与一维单多项式约束 `msg=6bebedde`；交 `@ProverDev` 执行 Stage 2 编码与评测，完成后交 `@Reviewer` Stage 3 审查）
- **关联任务**：`#code-and-bench:#112`（来源：`#code-and-bench:97e3eae4`）
- **对标清单**：Code-based PCS Zoo 编码器仓库 v2（`#1`–`#24`）

---

## 0. Jal1n 已拍板锁定的四项核心口径（`msg=45aff629` + `msg=6bebedde`）

1. **一维单多项式编码（严禁交织码与矩阵 Reshape，`msg=6bebedde`）**：
   - **只考虑单个多项式（1D 向量）的情形**：输入始终为一条长度为 $K = 2^k$ 个基域元素的一维向量 $x \in \mathbb{F}^{2^k}$（对应矩阵接口中的 `nrows = 1` 或 `width = 1`、`log_batch_size = 0`），经单次编码输出一条长度为 $N = 2^k / \rho = c \cdot 2^k$ 的一维码字 $w = \mathrm{Enc}(x) \in \mathbb{F}^{N}$。
   - **剔除所有交织码与二维矩阵 Reshape 码**：
     - 剔除 **Zoo `#2` 交织 RS（Ligero / ReedWeave / LiftWHIR）**；
     - 剔除 **Zoo `#4` Binius 块级/交织 RS**（一维二元加法 RS 已由 `#3` 覆盖）；
     - 剔除 **Zoo `#21` 张量积码 $C \otimes C$（TensorSwitch）**（张量码本质需将 $2^k$ 消息 reshape 成 $2^{k/2} \times 2^{k/2}$ 矩阵做行列二维编码）；
     - 其余所有码（RS、BaseFold RFC、HyperFold、Systematic QA、Brakedown/Spielman、EA、RAA、Bolt、Lightning、ERA、SPIN）**一律不将多项式 reshape 为二维矩阵**，直接作为输入长度 $K = 2^k$ 的一维线性码测试。
2. **有限域对齐策略（`unified_native`）**：
   - 采用 **“同域核心主表（素域统一 Goldilocks 64-bit，二元域统一 $\mathbb{F}_{2^{32}}$ & $\mathbb{F}_{2^{64}}/\mathbb{F}_{2^{128}}$）+ 各论文原生大素域/SIMD 附表”**。
3. **码率策略（`both_and_native`）**：
   - 常规码全测 **$\rho \in \{1/2, 1/4\}$**（$c \in \{2, 4\}$）；
   - 原生高码率 Sketched 码（Bolt $\rho=0.8$、Lightning $\rho \approx 0.78/0.63$）保留论文原生高码率并补测可调内码 $\rho_{\text{in}} \in \{1/2, 1/4\}$；
   - 半码率 SPIN 仅测其支持的固定 $\rho=1/2$。
4. **纳入 HyperFold / Binary-HyperFold（`include`）**：
   - 将 **HyperFold 与 Binary-HyperFold（$r \in \{2, 4, 8\}$，RS 与 QA 底码）** 一并纳入本次一维纯编码横评。

---

## 1. 统一评测规范

1. **计时边界（纯编码 `encode_ms`）**：
   - **仅计入**：一维输入向量 $x \in \mathbb{F}^{2^k}$ 生成一维码字 $w \in \mathbb{F}^{2^k/\rho}$ 的纯编码耗时。
   - **严格排除**：参数/稀疏图/随机置换/对角元/单位根表生成（单独记入 `setup_ms`）、随机输入生成、输出缓冲区首次缺页（warmup 阶段完成预分配与 touch）、Merkle 树哈希与打开证明。
2. **硬件、线程与采样**：
   - **硬件**：AMD EPYC 9754（503 GiB RAM），固定绑定 **32 物理核**（`taskset -c 0-31`，`RAYON_NUM_THREADS=32`，`OMP_NUM_THREADS=32`），**所有配置严格串行依次执行**（禁止并发跑多个基准）。
   - **采样**：每配置 **1 次 warmup + 3 次正式计时**，同时记录 **算术均值（`encode_mean_ms`）** 与 **中位数（`encode_median_ms`）**，并计算吞吐率 `throughput_melem_s`（$2^k / 10^6 / (\text{encode\_mean\_ms}/1000)$）与 `throughput_gib_s`（$\text{input\_bytes} / 2^{30} / (\text{encode\_mean\_ms}/1000)$）。
3. **多项式规模 $K = 2^k$ 与物理/算法上限**：
   - **标准规模网格**：$k \in \{20, 22, 24, 26, 28, 30\}$（步长 2，共 6 个规模点，$K = 2^k$ 为一维消息的基域元素个数）。
   - **明确记录的算法/内存边界**：
     - **BabyBear (31-bit) 一维乘法 NTT**：乘法子群二幂阶上限为 $2^{27}$，故一维码字长 $N = c \cdot 2^k \le 2^{27}$（$\rho=1/2$ 测至 $k=26$，$\rho=1/4$ 测至 $k=24$）；Goldilocks 二幂阶为 $2^{32}$，全量覆盖 $k \in \{20..30\}$、$\rho \in \{1/2, 1/4\}$。
     - **一维 EA（Expand–Accumulate）显式稀疏矩阵内存上限**：一维 EA 的稀疏矩阵 $E$ 含 $N \cdot d$ 个非零元（$N = c \cdot 2^k$，列重 $d = \log_2(N) \cdot 18 / c \approx 180\text{--}290$）。不 reshape 为矩阵时，显式存储 $E$ 在 $k=20, 22$（及 Goldilocks $k=24$）可装入内存，更大 $k$ 超过单机 420 GiB 内存上限时按实测/预估标记 `OOM_SKIPPED`（这正是 1D EA 相比 1D RAA/QA/RS 的真实内存特征，不强行改写协议）。
     - **`spin_codes` (`PacketRs8T64`)**：内部 32-bit 字节路由偏移上限要求 $K \le 2^{27}$，故 `PacketRs8T64` 测 $k \in \{20, 22, 24, 26\}$；原论文 `T128S19` (BCH+IMT) 支持 $k \in \{20..30\}$。
     - **`SIMD-Spielman`**：原仓库 CMake 生成的一维 Spielman 基准覆盖 $k \in \{20, 22, 24, 26\}$。
     - **单进程 420 GiB 内存保护**：256-bit 素域或大状态编码器在 $k=28, 30$ 若峰值内存超 420 GiB，标 `OOM_SKIPPED`。

---

## 2. 拟测一维编码清单与代码实现映射（共 15 组）

### Track A：素域一维编码（Prime Field 1D Codes，8 组）

| 序号 | Zoo # | 编码名称（1D 单多项式） | 测试有限域 | 测试码率 $\rho$ | 规模 $k$ ($\log_2 K$) | 选用代码仓库与 1D 调用入口 | 1D 32 线程实现要点 |
|---:|---|---|---|---:|---:|---|---|
| **A1** | `#1` | **RS（乘法 NTT Coset LDE）**<br>*(FRI / STIR / WHIR / DeepFold)* | Goldilocks (64b)<br>BabyBear (31b) | $1/2,\; 1/4$ | Gold: $20..30$<br>BB: $20..26/24$ | 本地 `/home/zjl/Plonky3`<br>(`p3-dft`: `Radix2DitParallel::coset_lde_batch`) | 传入 `RowMajorMatrix::new(msg, 1)`（单列高 $2^k$，`width=1`），`Radix2DitParallel` 自动在单列蝶形层内做 32 线程并行 |
| **A2** | `#5` | **随机可折叠码（BaseFold RFC, $r=2$）**<br>*(BaseFold / UltraFold)* | Goldilocks (64b)<br>M127 (127b) | $1/2,\; 1/4$ | $20, 22, 24, 26, 28, 30$ | 本地 `/home/zjl/plonkish_basefold`<br>(`basefold::encode`，另可用 `/home/zjl/ERA` `BasefoldCode` 对照) | 原生即为 1D 向量（底码 $k_0=64$ RS + $d=k-6$ 层 1D 随机对角蝶形，32 线程 Rayon 并行） |
| **A3** | `#5+` | **高阶超可逆可折叠码（HyperFold, $r \in \{2,4,8\}$）**<br>*(HyperFold)* | Goldilocks (64b)<br>M127 (127b) | $1/2,\; 1/4$ | $20, 22, 24, 26, 28, 30$ | 本地 `/home/zjl/HyperFold`<br>(`encoder::encode_top`，RS 底码与 QA 底码) | 原生即为 1D 向量（$H_2/H_4/H_8$ 无逆加法电路 + 递归 `butterfly_group` 32 线程并行） |
| **A4** | `#6` | **奇特征系统准阿贝尔码（1D Systematic QA / WHT）**<br>*(QAPCS / Quasar 1D 核)* | Goldilocks (64b)<br>M127 (127b) | $1/2,\; 1/4$ | $20, 22, 24, 26, 28, 30$ | 本地 `/home/zjl/HyperFold`<br>(`base_code::wht_in_place` + 随机对角缩放) | 对长 $2^k$ 的 1D 向量直接做 $\mathrm{Enc}(m)=(m, HD_1Hm, \dots, HD_{c-1}Hm)$；**注意**：需将 `wht_in_place` 外层循环在大块上启用 Rayon 并行（如递归 `rayon::join` 或 `par_chunks_exact_mut`），确保 1D 全长 WHT 吃满 32 线程 |
| **A5** | `#7` | **并列 Expand–Accumulate（1D EA）与素域 1D RAA**<br>*(EA PCS 1D 核)* | ① Goldilocks & `secp256k1` Fr<br>② Ristretto255 Fr (253b) | $1/2,\; 1/4$ | EA: $20..24^*$ (显式矩阵上限)<br>RAA: $20..30^*$ | ① `/home/zjl/ERA` (`EaCode<Goldilocks>` / `<SecpScalar>`)<br>② CRYPTO'24 `/tmp/scout-encoding.wtu0l0/EACode` (`profiler/encode.rs` `ea_encode` & `raa_encode`) | `msg_length = 2^k` 单条 1D 向量；`sparse_mat_mul` 开启 `parallel = true`（按 $c\cdot 2^k$ 个输出坐标 `into_par_iter` 并行），后接 1D 前缀和累加 |
| **A6** | `#12` | **1D Brakedown / 广义 Spielman 稀疏码**<br>*(Brakedown / Spielman)* | ① Goldilocks & `secp256k1`<br>② `Ft127` (127b)<br>③ Mersenne61 / Monty64 | ① $1/2,\; 1/4$<br>② 论文原生 $\approx 0.657/0.581$ | ①② $20..30^*$<br>③ $20..26$ | ① `/home/zjl/ERA` (`BrakedownCode` 1D) + `/home/zjl/plonkish_basefold`<br>② `/home/zjl/lcpc` (`lcpc-brakedown-pc::encode` 1D)<br>③ `/tmp/scout-encoding.wtu0l0/simd-spielman` (`*_MT_*` 1D) | 对单条长 $2^k$ 向量做递归 $A \to \mathrm{Enc} \to B$；在 `ERA::BrakedownCode::Expander::apply` 中对输出顶点开启 Rayon 并行；`SIMD-Spielman` 跑单码字多线程二进制 |
| **A7** | `#13` | **1D Lightning（LDPC Sketch + 1D Brakedown 内码）**<br>*(Lightning 1D 核)* | BN254 Fr (254b, `mcl`) | 原生 $\rho \approx 0.78/0.63$<br>+ 调 $\alpha$ 对齐 $1/2$ | $20..28, (30^*)$ | 官方 `/tmp/scout-zoo.FqL9pS/Lightning`<br>(`lightning.cpp` 固定 `ROW_NUMBER = 1, COLUMN_NUMBER = 2^k`) | 取消矩阵分块，令 `ROW_NUMBER = 1`，对单条 $2^k$ 向量测 `LDPC aggregate + 1D Brakedown inner encode` |
| **A8** | `#20` | **1D ERA（Encode–Repeat–Accumulate）**<br>*(ERA 1D 核)* | Goldilocks (64b)<br>`secp256k1` Fr (256b) | $\approx 1/2$ ($r=2$)<br>$\approx 1/4$ ($r=4$) | $20..30^*$ | 本地 `/home/zjl/ERA`<br>(`EraCode::encode_era` / `OptimizedEraCode`，取 `seg_count = 1, seg_msg_size = 2^k`) | 单条长 $2^k$ 向量经 1D Brakedown 基码（$\rho_B=1/1.05$）+ 重复 $r \in \{2,4\}$ + 两轮 1D 置换、对角乘与前缀和 |

---

### Track B：二元域一维编码（Binary Field 1D Codes，7 组）

| 序号 | Zoo # | 编码名称（1D 单多项式） | 测试有限域 | 测试码率 $\rho$ | 规模 $k$ ($\log_2 K$) | 选用代码仓库与 1D 调用入口 | 1D 32 线程实现要点 |
|---:|---|---|---|---:|---:|---|---|
| **B1** | `#3` | **1D 二元加法 RS（Additive NTT: LCH14 / PolyBasis）**<br>*(FRI-Binius / Binary WHIR / Ligerito)* | $\mathbb{F}_{2^{32}}, \mathbb{F}_{2^{64}}, \mathbb{F}_{2^{128}}$ | $1/2,\; 1/4$ | $20, 22, 24, 26, 28, 30$ | ① 主测：`/home/zjl/Plonky3` (`p3-binary-dft`: `AdditiveRsEncoder` LCH & PolyBasis)<br>② 对照：`/home/zjl/bolt-rs` (`ReedSolomonEncoding::encode_non_systematic`) | `p3-binary-dft` 传入 `RowMajorMatrix::new(msg, 1)`（单列 `width=1, height=2^k`），内部 `staging.rs` 已针对单列做跨层 tile 32 线程并行 |
| **B2** | `#6` | **1D 特征二系统准阿贝尔码（1D Binary QA）**<br>*(Castor / `p3-binary-qa`)* | $\mathbb{F}_{2^{32}}, \mathbb{F}_{2^{64}}, \mathbb{F}_{2^{128}}$<br>*(同域 & 子域见证混合)* | $1/2,\; 1/4$ | $20, 22, 24, 26, 28, 30$ | 本地 `/home/zjl/zkp-research/plonky3-binary-qa/binary-qa`<br>(`QaEncoder::encode(&msg)` 即 `log_batch_size = 0, width = 1`，及 `subfield_encode_batch(&msg, 0)`) | `QaEncoder::encode` 原生就是 `width=1, log_message_len=k` 的单多项式 1D 编码，且内部 `layers::<S, false, true>` 与 `multiply_spectrum` 已自带 32 线程 Rayon 并行！ |
| **B3** | `#5+` | **1D 二元高阶可折叠码（Binary HyperFold, $r \in \{2,4,8\}$）**<br>*(Binary HyperFold)* | $\mathbb{F}_{2^{64}}, \mathbb{F}_{2^{128}}$<br>*(及 BF32/BF16 原生)* | $1/2,\; 1/4$ | $20, 22, 24, 26, 28, 30$ | 本地 `/home/zjl/zkp-research/binary-hyperfold`<br>(`code::native` / `code::folding`，加法 RS 底码 `AdditiveRsEncoder`) | 原生即为单条 $2^k$ 多项式的一维高阶折叠编码（仅加法 RS 底码，无 QA 底码，32 线程并行），与 B1 (1D RS)、B2 (1D QA) 同域同输入长度直接横评 |
| **B4** | `#9` | **1D Bolt Sketched Code（`bolt-xor` & `bolt32`）**<br>*(Bolt 1D 核)* | $\mathbb{F}_{2^{32}}$ (`BinaryElem32`) | 原生 $\rho = 0.8$<br>+ 内码 RS $1/2, 1/4$ | $20, 22, 24, 26, 28, 30$ | 官方 `/home/zjl/bolt-rs`<br>(`ColMajorMatrix` 设 `nrows = 1, m = 2^k`：`ExpanderMatrix` + 1D RS) | `nrows = 1` 时：`ExpanderMatrix` 按 $2^{k-3}$ 个约束输出列做 Rayon 32 线程并行，后接对长 $2^{k-3}$ 摘要的一维 RS 编码 |
| **B5** | `#11` | **1D 二元打包 RAA（Packed Binary RAA）**<br>*(Blaze / Bolt 1D RAA)* | ① $\mathbb{F}_{2^{32}}, \mathbb{F}_{2^{128}}$ (`bolt-rs`)<br>② 64b 字 `Blazeu64` | $1/2,\; 1/4$<br>*(重复 $q \in \{2,4\}$)* | $20, 22, 24, 26, 28, 30$ | ① 主测：`/home/zjl/bolt-rs` (`raa::raa_encode_auto`，设 `nrows = 1, msg_len = 2^k`)<br>② 对照：`/home/zjl/plonkish_basefold` (`raa::encode_bits` 1D) | `bolt-rs` 在 `nrows = 1` 时：`raa_repeat` 与 `raa_permute_columns` 仍按 $q\cdot 2^k$ 列做 32 线程并行分块，`raa_prefix_xor` 做 1D 顺序前缀 XOR |
| **B6** | `#12` | **1D 二元域 Brakedown 稀疏码**<br>*(Bolt 1D Brakedown)* | $\mathbb{F}_{2^{32}}$ (`BinaryElem32`) | 原生 $\rho \approx 0.506/0.674$<br>+ 配置 $1/2, 1/4$ | $20, 22, 24, 26, 28, 30$ | 官方 `/home/zjl/bolt-rs`<br>(`BrakedownEncoder::encode`，设 `nrows = 1, msg_len = 2^k`) | `nrows = 1` 时各递归层 `ExpanderMatrix` 按输出约束列 32 线程并行，与 B1、B2、B4、B5 在 $\mathbb{F}_{2^{32}}$ 一维同台对比 |
| **B7** | `#19` | **1D SPIN 二元线性码（BCH+IMT & Packet-RS8）**<br>*(SPIN 1D 核)* | 128-bit 二元记录 (`Block`, 等价 $\mathbb{F}_{2^{128}}$ 位切片) | 固定 $\rho = 1/2$ | `T128S19`: $20..30$<br>`PacketRs8T64`: $20..26$ | 官方 `/tmp/scout-encoding.wtu0l0/spin_codes/spin`<br>(`spin::Code` 设 `message_size = 2^k`，测 `forward` 与 `transpose_inplace`) | 直接构造单码字 `CodeSpec{.message_size = 1ULL << k}`（不拆多行），实测单条 $2^k$ 记录的一维正向与转置编码耗时 |

---

## 3. Zoo `#1`–`#24` 中不纳入本次一维横评的 12 个条目归类

1. **因属于交织码或需将多项式 Reshape 成二维矩阵而排除（3 条，遵照 `msg=6bebedde`）**：
   - **Zoo `#2` 交织 RS（Ligero / ReedWeave / LiftWHIR）**
   - **Zoo `#4` Binius 块级/交织 RS**（一维加法 RS 已由 B1 `#3` 覆盖）
   - **Zoo `#21` 张量积码 $C \otimes C$（TensorSwitch）**（需 reshape 为 $\sqrt{K} \times \sqrt{K}$ 二维网格）
2. **无公开可访问编码器或非单一线性码（9 条）**：
   - **`#8` Gabidulin (qFFT)**（匿名链接 403）、**`#10` Exact-weight EA (Flare)**（无公开仓库，算子由 A5 覆盖）、**`#14` Bolt 理论线性码**（无独立实现）、**`#15` 盲化/FHE 加权 RAA**（无公开仓库）、**`#16` BA-3 / Chosen-Block BAA**（依赖的私有 `ladnir/libOTe` 404）、**`#17` 大域 Addition-only Block+Accumulate**（无公开代码）、**`#18` RAAA 三次累加**（无公开代码）、**`#22` RM+KU 预处理**（无公开代码）、**`#23` SmallWood DECS/LVCS**（非单一线性纠错码）、**`#24` $s$-projected Goppa**（无公开代码）。

---

## 4. Stage 2 (`@ProverDev`) 执行交付物与极简验证要求

1. **实验目录与输出文件**：`~/zkp-research/experiments/code-encoding-bench-2026-11-21/`
   - `results/prime_goldilocks_1d.csv`：**主表 1（64-bit Goldilocks 一维纯编码统一横评）**，覆盖 A1(1D RS)、A2(BaseFold RFC)、A3(HyperFold $r=2,4,8$)、A4(1D QA/WHT)、A5(1D EA & 1D RAA)、A6(1D Brakedown)、A8(1D ERA)，$k \in \{20..30\}$，$\rho \in \{1/2, 1/4\}$。
   - `results/binary_1d.csv`：**主表 2（二元域 $\mathbb{F}_{2^{32}}$ 与 $\mathbb{F}_{2^{64}}/\mathbb{F}_{2^{128}}$ 一维纯编码统一横评）**，覆盖 B1(1D 加法 RS LCH/PolyBasis)、B2(1D Binary QA)、B3(Binary HyperFold $r=2,4,8$)、B4(1D Bolt `bolt-xor`/`bolt32`)、B5(1D 打包 RAA)、B6(1D 二元 Brakedown)、B7(1D SPIN `T128S19`/`PacketRs8T64`)，$k \in \{20..30\}$，$\rho \in \{1/2, 1/4\}$ 及原生高码率。
   - `results/native_fields_1d.csv`：**附表 3（各论文原生大素域 / 小素域 / AVX-512 SIMD 工件一维实测）**，覆盖 BabyBear 1D RS、M127 (BaseFold RFC / HyperFold / 1D WHT-QA)、`Ft127` (`lcpc` 1D Brakedown)、Ristretto255 (`EACode` 1D EA & RAA)、`secp256k1` (`ERA` 1D ERA / BaseFold / Brakedown / EA)、BN254 (`Lightning` 1D)、`SIMD-Spielman` (EPYC 9754 AVX-512 IFMA 1D, $k \in \{20..26\}$)。
   - `REPORT.md`：汇总上述三张 Markdown 对比表、关键吞吐率观察与排除说明。
2. **统一 CSV 列定义**：
   ```text
   table_id,zoo_id,code_family,variant,repo,field,field_bits,k,input_elements,input_bytes,nominal_rate,actual_rate,codeword_elements,threads,setup_ms,encode_mean_ms,encode_median_ms,throughput_melem_s,throughput_gib_s,peak_rss_gib,status,notes
   ```
3. **三不原则与极简正确性检查**：
   - 不建跨仓库重型抽象框架；直接在实验目录下用轻量 Rust/C++ driver 或各仓库薄封装 binary 输出统一 CSV 行。
   - 正确性检查只做 happy-path：① 断言输出一维码字长度 `codeword_elements == expected` 且非全零；② 对新增/薄改的 1D 算子（如 1D 并行 WHT-QA、1D 并行 EA/Brakedown）在 $k=10$ 上做一次线性性检验 $\mathrm{Enc}(a+b) = \mathrm{Enc}(a)+\mathrm{Enc}(b)$ 或 `matches_naive`。
