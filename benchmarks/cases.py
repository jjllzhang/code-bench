"""Build the requested single-message measurement grid."""
from collections import OrderedDict
from math import ceil

SIZES = (20, 22, 24, 26, 28, 30)
FIELDS = {"goldilocks": 64, "babybear": 31, "m127": 127, "secp256k1": 256,
          "ristretto255": 253, "ft127":127, "bn254":254, "m61":61, "monty64":64,
          "bf16":16, "bf32":32, "bf64":64, "bf128":128, "block128":128}
REPOS = {
    "p3":"Plonky3/Plonky3@0d803737b681774186cd283b1fd2d8e493655c82",
    "qa":"jjllzhang/plonky3-binary-qa@19affa0a8de1b283e766556b757725c701397657",
    "hyperfold":"jjllzhang/HyperFold@405b2094c70747af6e4b1ae05aa0661bf6c7b9a9",
    "binary-hyperfold":"jjllzhang/binary-hyperfold@80f16b8e32da3d2b2478b8e075f5095c8ae8c8cb",
    "era":"ERA local source snapshot",
    "basefold":"plonkish_basefold@c29f08653121637b456e4705d901d078cd6fc668",
    "bolt":"bolt-rs@3832e47b24e7b3e10525c9c5bcfc1cfe66d525f2 with local 1D driver",
    "ea":"EACode CRYPTO’24 artifact",
    "lcpc":"lcpc@f0e2116001af5a1bbf39481535f837d6a25772e8",
    "spin":"spin_codes@584a7fb654e824bf296aeb92ef7c6edd92e63fc2",
    "simd":"simd-spielman@7b399dbfecc406c79349015f1e21accc4def1be7",
    "lightning":"Lightning@08dbd81b0785c78704b9dafc0315d793760a97fe",
}


def oom(needed, label):
    if needed >= 420 << 30:
        return "OOM_SKIPPED", f"{label} lower bound {needed/(1<<30):.1f} GiB."
    return "", ""


def era_graph_bytes(n, ratio, alpha, cn, dn, element):
    edges = 0
    while n > 32:
        y = ceil(alpha*n)
        z = int(y * ratio)
        if y < cn or int(n * ratio) - n - z < dn:
            break
        edges += n * cn + z * dn
        n = y
    # Every retained edge is a native word index and a field element.
    return edges * (8 + element)


def era_memory(k, c, field, era=False):
    n = 1 << k
    width = 8 if field == "goldilocks" else 32
    if era:
        base = int(n * 1.05)
        graph = era_graph_bytes(n, 1.05, 0.04, 8, 64, width)
        return oom(graph + n*width + c*base*2*(8+width), "Retained ERA graph, permutations and weights")
    graph = era_graph_bytes(n, c, 0.3, 14, 28, width)
    return oom(graph + n*width, "Retained Brakedown graph and message")


def bolt_brakedown_memory(k, c, _):
    n = 1 << k
    ratio = {"native-high":1/0.674, "native-low":1/0.506}.get(c, c)
    edges = 0
    top = n
    while n > 64:
        y = round(.238 * n)
        z = round(ratio * y)
        edges += n*13 + z*14
        n = y
    return oom(edges * 16 + (top + round(ratio * top)) * 4,
               "Retained weighted graph and input/output")

def grid():
    all_cases = OrderedDict()

    def add(table, zoo, family, variant, repo, field,
            executable, operation, params=(), rates=(2, 4), limit=None,
            metadata="", sizes=SIZES, launch_threads=32):
        for k in sizes:
            for c in rates:
                cid = "-".join(map(str, (table, family, variant, field, k, c)))
                if cid in all_cases:
                    raise ValueError(cid)
                status, notes = limit(k, c, field) if limit else ("", "")
                field_bits = FIELDS[field.split("-")[0]]
                all_cases[cid] = dict(id=cid, table_id=table, zoo_id=zoo, code_family=family,
                                      variant=variant, repo=REPOS[repo], field=field,
                                      field_bits=field_bits, k=k, rate=c,
                                      executable=executable, command=[operation, field, str(k), str(c), *map(str, params)],
                                      status=status, notes=" ".join(filter(None, (metadata, notes))),
                                      threads=launch_threads)
    def bb(k, c, _):
        return ("DOMAIN_LIMIT", "Need k+log2(c) <= 27.") if (1 << k)*c > 1 << 27 else ("", "")

    for field, tab in (("goldilocks","prime_goldilocks_1d"), ("babybear","native_fields_1d")):
        add(tab, "1","rs","p3-coset-lde","p3",field,"core","rs",limit=bb if field=="babybear" else None,
            metadata="Single-column coset LDE from input evaluations. Owned output buffer reused.")
    for field, tab in (("goldilocks","prime_goldilocks_1d"), ("m127","native_fields_1d")):
        for r in (2, 4, 8):
            for base in ("rs", "qa"):
                add(tab,"5+","hyperfold",f"r{r}-{base}","hyperfold",field,"core","hyperfold",(r,base))
        add(tab,"6","qa","packed-wht","hyperfold",field,"core","qa",
            metadata="Benchmark-only parallel WHT, upstream packed butterflies. Fixed nonzero spectral units.")
        add(tab,"5","basefold","rs64-rfc","basefold",field,"plonkish","basefold",
            metadata="Original field representations (Goldilocks occupies 16 B) and RS base encoder. Input coefficients.",
            limit=lambda k,c,f: ("DOMAIN_LIMIT","Original AES-CTR32 table stream cannot emit 2^32 blocks.")
                if k==30 and c==4 and f=="m127" else ("",""))

    for field in ("bf32","bf64","bf128"):
        add("binary_1d","3","additive-rs","lch","p3",field,"core","lch")
        add("binary_1d","3","additive-rs","polybasis","p3",field,"core","poly",
            limit=lambda k,c,f: ("UNSUPPORTED_BACKEND","Stock PolyBasisNtt implements BinaryField128 only.")
                if f!="bf128" else ("",""))
    for field in ("bf32","bf64","bf128","bf32-bf64","bf32-bf128","bf64-bf128"):
        add("binary_1d","6","qa","binary-spectral","qa",field,"core","qa",
            metadata="One coefficient vector, log_batch_size=0. Hyphenated fields give input and codeword alphabets.")
    for field in ("bf16","bf32","bf64","bf128"):
        for r in (2, 4, 8):
            add("binary_1d","5+","binary-hyperfold",f"r{r}-rs","binary-hyperfold",field,"core","hyperfold",(r,),
                metadata="Default admissible mu0 rule. Encoder geometry only.")

    def ea_limit(k, c, field):
        stride = 24 if field == "goldilocks" else 48
        entries = ((k+c.bit_length()-1)*18//c)*c*(1<<k)
        cap = 420 << 30
        base = (1+c)*(1<<k)*(8 if field=="goldilocks" else 32)
        needed = entries*stride + base
        if needed >= cap:
            return "OOM_SKIPPED", f"Explicit matrix plus message/output lower bound {needed/(1<<30):.1f} GiB."
        return "", ""
    for field, tab in (("goldilocks","prime_goldilocks_1d"), ("secp256k1","native_fields_1d")):
        add(tab,"7","ea","ea-explicit","era",field,"era","ea",limit=ea_limit)
        add(tab,"7","raa","raa-unweighted","era",field,"era","raa")
        add(tab,"12","brakedown","brakedown-recursive","era",field,"era","brakedown",limit=era_memory)
        add(tab,"20","era","brakedown-repeat-accumulate","era",field,"era","era",
            metadata="Nominal repetition 2/4. Actual rate includes 1.05x inner Brakedown.",
            limit=lambda k,c,f: era_memory(k,c,f,era=True))
    for code in ("ea","raa"):
        add("native_fields_1d","7",code,"eacode-official","ea","ristretto255","eacode",code,
            limit=ea_limit if code=="ea" else None, launch_threads=32 if code=="ea" else 1)
    for f,tab in (("goldilocks","prime_goldilocks_1d"), ("m127","native_fields_1d")):
        add(tab,"12","brakedown","plonkish-sdig3","basefold",f,"plonkish","brakedown",
            rates=("native",), launch_threads=1,
            metadata="Native BrakedownSpec3, original serial 1D encode. Field element occupies 16 bytes.")
    for variant in ("sdig3","sdig2"):
        add("native_fields_1d","12","brakedown",variant,"lcpc","ft127","lcpc",variant,rates=("native",),launch_threads=1,metadata="Stock sparse multiply is serial for one codeword.")
    for field in ("m61","monty64"):
        add("native_fields_1d","12","spielman","simd-mt","simd",field,"simd","spielman",rates=("native",),
            limit=lambda k,c,f: ("EXCLUDED_INTERLEAVED","Official SIMD harness processes independent codewords in parallel columns."))
    add("native_fields_1d","13","lightning","ldpc-brakedown","lightning","bn254","lightning","lightning",
        rates=("native-high","native-low","half"),launch_threads=1,
        metadata="Original uint64 input and BN254 operations. Sparse aggregation and inner encoder are serial.")
    add("binary_1d","3","additive-rs","bolt-rs","bolt","bf32","bolt","rs",launch_threads=1,
        metadata="Stock per-codeword RS kernel is serial under the 32-core affinity.")
    for variant in ("bolt-xor","bolt32"):
        add("binary_1d","9","bolt",variant,"bolt","bf32","bolt",variant,rates=(2,4),
            metadata="Requested rate applies to inner RS. Actual rate includes systematic input.")
    for field in ("bf32","bf128"):
        add("binary_1d","11","raa","bolt-raa","bolt",field,"bolt","raa")
    add("binary_1d","11","raa","blaze-packed-u64","basefold","bf64","plonkish","raa",
        metadata="64-bit packed binary record, not a field multiply representation.")
    add("binary_1d","12","brakedown","bolt-binary","bolt","bf32","bolt","brakedown",rates=(2,4,"native-high","native-low"),limit=bolt_brakedown_memory,
        metadata="Native-rate labels are target ratios with fixed alpha and graph degrees.")
    for variant in ("imt","packet"):
        add("binary_1d","19","spin",variant,"spin","block128","spin",variant,rates=(2,),
            limit=lambda k,c,f: ("DOMAIN_LIMIT","32-bit byte route bounds.") if variant=="packet" and k>26 else ("",""),
            metadata="128-bit binary records. Stock forward single-codeword transform is serial.", launch_threads=1)
    return sorted(all_cases.values(), key=lambda c:(c["k"], c["id"]))


if __name__ == "__main__":
    import json
    print(json.dumps(grid(), indent=2))
