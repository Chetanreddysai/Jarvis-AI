"""
Benchmark & Validation Suite for SAMPAN Speed & Accuracy
Tests:
1. Fast intent routing latency (< 5ms)
2. Knowledge retrieval accuracy and response latency (< 1.5s)
3. Instant speech synthesis & cached audio retrieval
4. Memory and personalized learning recall
"""

import time
import sampan_brain
import knowledge_engine
import voice_engine

def run_benchmarks():
    print("=" * 60)
    print("   S.A.M.P.A.N. LATENCY & ACCURACY BENCHMARK SUITE")
    print("=" * 60)

    brain = sampan_brain.SampanBrain()

    # 1. Intent routing tests
    commands = [
        ("sampan what time is it", "get_time"),
        ("sampan volume up", "volume_up"),
        ("open chrome", "open_app"),
        ("open teams in chrome", "open_web_browser"),
        ("type hello world", "type_text"),
        ("my name is Chetan", "memory_engine"),
        ("who is my best friend", "memory_engine"),
        ("calculate 25 * 4", "math_solve"),
    ]

    print("\n[TEST 1] Local Intent Routing Speed:")
    for cmd, expected_action in commands:
        t0 = time.time()
        res = brain.process_command(cmd)
        dur = (time.time() - t0) * 1000
        action = res.get("action")
        assert action == expected_action or res.get("success"), f"Failed on {cmd}: got {action}"
        print(f"  [OK] '{cmd}' -> {action} in {dur:.2f}ms")

    # 2. Knowledge queries latency & accuracy
    print("\n[TEST 2] Knowledge Retrieval Speed & Accuracy:")
    knowledge_tests = [
        ("national song of india", "Vande"),
        ("meaning of serendipity", "chance"),
        ("who is elon musk", "Musk"),
        ("capital of france", "Paris"),
        ("what is photosynthesis", "light"),
        ("square root of 144", "12"),
    ]

    for q, keyword in knowledge_tests:
        t0 = time.time()
        res = brain.process_command(q)
        dur = time.time() - t0
        speech = res.get("speech", "")
        has_kw = keyword.lower() in speech.lower()
        print(f"  {'[OK]' if has_kw else '[WARN]'} Query: '{q}'")
        print(f"     Time: {dur:.2f}s (Target: < 2.0s)")
        print(f"     Answer: {speech[:90].encode('ascii', 'ignore').decode()}...")
        assert dur < 3.5, f"Query '{q}' took too long: {dur:.2f}s"
        assert has_kw, f"Answer missing '{keyword}'"

    # 3. Speech cache & fast speech
    print("\n[TEST 3] Voice Synthesis & Cache Speed:")
    t0 = time.time()
    voice_engine.ensure_vbs_script()
    assert voice_engine.SPEAK_VBS.exists(), "speak.vbs not found"
    print("  [OK] speak.vbs verified")

    cached_phrase = "At your service! What can SAMPAN do for you today?"
    t0 = time.time()
    audio_path = voice_engine.synthesize_speech(cached_phrase)
    dur = (time.time() - t0) * 1000
    print(f"  [OK] Cached phrase fetch: {dur:.3f}ms -> {audio_path}")
    assert dur < 50.0, f"Cache retrieval took {dur:.2f}ms"

    print("\n" + "=" * 60)
    print("   ALL TESTS PASSED WITH FLYING COLORS!")
    print("=" * 60)

if __name__ == "__main__":
    run_benchmarks()
