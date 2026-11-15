# Lóng direction — final MP4 visual review

Reviewed 12/11/2026. File: `final.mp4`; SHA256 `b6fa87ebf7e27266f1ac7471a47852e116aeb1f2628cecfdb409d8c0aac7156c`.

All 38 clauses pass the **sampled core-meaning check**. I re-opened all 10 phrase/frame pairing sheets derived from this actual final MP4, all three operation strips, and three additional chunk-boundary sheets. These are actual visible observations, not acceptance inferred from renderer code or successful decode. Detailed per-shot observations and fresh evidence hashes are in `qa/semantic-review.json`.

The previous semantic fixes are visible in the actual file:

- Email scenes use `khach@vidu.invalid`, Mẫu A, an explicit draft state and a locked send control. The opening draft contains “Mua ngay!” before its later tone comparison. No sampled email state implies successful sending.
- “Dùng không dây” is compared directly with the illustrated lamp's wire and hypothetical USB-C/có dây/không pin source. The wrong 120.000 đồng is compared with the same item's hypothetical 1.200.000 đồng source. These are labelled example values, not verified product facts.
- The handoff shows the actual wrong wireless claim crossed out beside the wired/no-battery source. The tone comparison calls “Mua ngay!” a forceful tone and presents “Mời bạn tham khảo.” as the alternative.
- The missing-context example states the customer's need to use the lamp where there is no outlet, beside Mẫu A's wired requirement and the overly broad “Phù hợp mọi góc làm việc” claim. The conflict is visible rather than represented by an unrelated person/photo.
- The 3D steps contain envelope/checklist/person icons and readable labels. Their focus progresses through creating, checking and deciding. They are symbolic diagrams with depth; they are not full email/source-document textures or a demonstrated real approval action.
- The final comparison uses the same whole task and standard: 12 minutes manually versus 2 minutes drafting plus 13 checking/fixing, 15 total. Remaining errors and insufficient evidence retain a blocked/unapproved state.
- The comment field demonstrates a specific example and the closing card shows the subscribe CTA with the three work steps. The illustrated interfaces do not perform a real send, comment or subscription.

Operation samples show prompt text revealing between 0.23 and 1.23 seconds and comment text progressing at 75.10, 75.90 and 76.67 seconds. The tone edit appears as readable before/after panels, not a literal deleting/typing operation in the sampled frames. Large time counters count up toward 13 and 15 while the example log already shows those final values. This is illustrative animation, not a stopwatch or measured working session.

I additionally inspected 81 actual frames: one frame before, at, and after every 3-second chunk boundary from 3 to 81 seconds. No black frame, empty-plane reset or abrupt state jump was visible in those samples. Evidence: `qa/chunk-boundaries-01.jpg` through `-03.jpg` and `qa/chunk-boundaries.json`.

Technical QA separately records 2460 decoded frames, 82 seconds, 1920×1080 at 30 fps. This review does not claim manual audio listening, continuous playback, inspection of every animation frame, or user aesthetic acceptance. The UI reconstructions and hypothetical values must remain identified as illustrations. User feedback is still pending.
