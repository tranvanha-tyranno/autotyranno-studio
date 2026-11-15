# Mô phỏng phải làm rõ điều gì — 24 đoạn

Thiết kế biên tập, chưa phải kiểm bản dựng. 19/24 đoạn có mô phỏng mang thông tin; 5 đoạn footage làm điểm chuyển/nghỉ có nội dung. Cues là câu nguyên script, phải gắn vào audio OpenAI mới.

Không tăng thông tin bằng cách dán thêm đoạn chữ. Mỗi cảnh có vật/đại lượng, thao tác và kết quả đổi. Không nhân vật hoạt hình, không subtitle, không giả mạo nguồn/branding.

## b01 · money_split

Visualize the opening paradox before explaining it.

**Cần thấy:** The same loaf has price+2,000 while the shop remainder falls500; the two arrows must not imply aggregate national outcomes.

**Mở cảnh:** One bread on an actual counter; two money routes are still connected to that same bread.

- “Ổ bánh tăng hai nghìn.” → The price tag changes20,000→22,000 and the extra2,000 travels out of the buyer side. → Customer outlay rises2,000.
- “người bán lại giữ được ít hơn năm trăm đồng” → The seller remainder changes3,000→2,500 and a500 difference leaves the remainder. → Customer outlay and seller retained amount move in opposite directions.
- “Vì sao cả hai vẫn thấy khó hơn?” → Keep only the two conflicting outcomes and the same bread, opening the unanswered route between them. → A concrete unresolved relation, not a title card.

**Phạm vi:** Ví dụ minh họa

**Dữ liệu:** {"priceBefore": 20000, "priceAfter": 22000, "remainderBefore": 3000, "remainderAfter": 2500, "difference": -500}

- Tránh: Do not call the remainder net profit.
- Tránh: Do not display all future wage/CPI information in the hook.

## b02 · real footage

Orient the single bakery story and plant the three objects that will return.

**Cần thấy:** Real hands prepare one consistent bread type; price board, receipt and pay envelope become three distinct points of inquiry.

**Mở cảnh:** Actual bakery preparation; footage people remain unnamed illustrative people.

- “tiệm bánh giả định của chị Hạnh” → Use a short in-scene hypothetical label without a disclaimer screen. → Scope established inside the story.
- “bảng giá, hóa đơn đầu vào, và tiền người mua kiếm được” → Briefly show the corresponding three objects in that spoken order. → Three concrete objects, not three abstract dashboard cards.

**Phạm vi:** Tiệm giả định; footage là bối cảnh

**Dữ liệu:** {}

- Tránh: Never identify stock staff as Hạnh or claim their real finances.

## b03 · money_split

Make the baseline arithmetic spatial and causal.

**Cần thấy:** 20,000 physically divides into12,000 variable costs,5,000 fixed allocation and3,000 remainder.

**Mở cảnh:** An intact20,000 strip/stack enters at the payment point; one bread pins the unit of analysis.

- “một ổ bán hai mươi nghìn” → Show the whole20,000 payment before splitting. → The viewer knows the total and unit.
- “hết mười hai nghìn” → Route12,000 into ingredients/variable costs. → 8,000 still unallocated.
- “được chia ra năm nghìn một ổ” → Take5,000 into fixed allocation; the quantity/sales assumption stays pinned. → 3,000 remains after the modeled costs.
- “Còn ba nghìn.” → Isolate the physical3,000 remainder without a profit label. → Arithmetic has unfolded, not appeared as a completed table.

**Phạm vi:** Ví dụ minh họa · cùng lượng bán giả định

**Dữ liệu:** {"price": 20000, "variable": 12000, "fixedAllocated": 5000, "remainder": 3000, "salesVolume": "held_constant_assumption"}

- Tránh: Do not show12k+5k+3k exceeding20k.
- Tránh: No continuously running counter after it reaches a meaningful state.

## b04 · cost_ledger

Limit the interpretation of the preceding result.

**Cần thấy:** 3,000 is an unfinished subtotal with tax, depreciation and owner labor not yet counted.

**Mở cảnh:** Reuse the3,000 subtotal from b03; a real receipt or ledger surface supplies context.

- “Khoan gọi ba nghìn ấy là tiền bỏ túi.” → Stop the3,000 moving toward an owner pocket; reopen it as an unfinished subtotal. → The remainder is explicitly provisional.
- “thuế, khấu hao và công của chủ tiệm” → Add three unpriced/unfilled ledger lines, not invented costs. → Viewer sees what the model excludes.
- “so trước với sau” → Pin the same scope to both before/after states. → Comparison remains valid only within this limited model.

**Phạm vi:** Khoảng dư mô hình · chưa phải lợi nhuận ròng

**Dữ liệu:** {"subtotal": 3000, "excludedUnpricedItems": ["thuế", "khấu hao", "công chủ tiệm"]}

- Tránh: No invented numeric tax, depreciation or wages.
- Tránh: Do not make the exclusions smaller than can be read at phone size.

## b05 · money_split

Show the pressure and the shop decision as separate states.

**Cần thấy:** First keep sale20,000 with cost14,500+5,000 to leave500; only then raise sale22,000 to leave2,500.

**Mở cảnh:** Same bread and fixed allocation as b03; variable-cost route is ready to expand.

- “thành mười bốn nghìn năm trăm” → Variable cost grows12,000→14,500 while sale is still20,000. → Remainder shrinks3,000→500.
- “Nếu giữ giá cũ” → Pause on the20,000 sale/500 remainder result. → The counterfactual is legible before the decision.
- “đổi bảng lên hai mươi hai nghìn” → Sale changes20,000→22,000;2,000 refills part of the lost remainder. → Remainder recovers500→2,500 but remains below3,000.
- “đầu vào đã tăng hai nghìn năm trăm” → Lay +2,000 received against +2,500 costs. → 500 gap explains the paradox.

**Phạm vi:** Ví dụ minh họa · cùng lượng bán giả định

**Dữ liệu:** {"oldPrice": 20000, "newVariable": 14500, "fixedAllocated": 5000, "oldPriceRemainder": 500, "newPrice": 22000, "newRemainder": 2500}

- Tránh: Do not reveal2,500 before narration says price is raised.

## b06 · money_split

Prove the destination of the extra payment.

**Cần thấy:** A2,000 increment enters the expanded cost stream but cannot fill the whole2,500 expansion.

**Mở cảnh:** Keep b05 routes and visually follow only the incremental money.

- “từ ba nghìn, tiệm chỉ còn hai nghìn năm trăm” → Before/after remainders align to the same baseline. → A500 shortfall is seen directly.
- “Hai nghìn tăng thêm không biến mất.” → The highlighted2,000 travels visibly into the2,500 extra-cost requirement. → The money has an explained destination.
- “Nó chưa bù hết phần chi phí tăng.” → Leave the500 uncovered notch in the extra-cost route. → The explanatory result appears as a physical gap, not a slogan.

**Phạm vi:** Ví dụ minh họa · khoản dư, chưa phải lãi ròng

**Dữ liệu:** {"saleIncrement": 2000, "costIncrement": 2500, "uncoveredIncrement": 500, "remainders": [3000, 2500]}

Footage nối: Return to a real receipt/ingredient action once the incremental route is understood.

- Tránh: Do not repeat the entire baseline calculation from zero.

## b07 · real footage

Release the graphic and ask the next unresolved question.

**Cần thấy:** Actual bread purchase, then the existing22,000 price board; alternative shop outcomes must be framed as possibilities.

**Mở cảnh:** Real hand-to-counter transaction or bread finishing, without invented identities.

- “muốn kết luận phải có sổ thật” → The illustrative ledger withdraws; real-world context is shown without asserting a particular shop outcome. → Scope of inference is clear.
- “tại sao bảng giá không quay về hai mươi nghìn?” → A20,000 reference mark appears beside the present22,000 label without resetting it. → The new question is rate versus level.

**Phạm vi:** Bối cảnh minh họa

**Dữ liệu:** {}

- Tránh: Do not fabricate news screenshots or current official inflation numbers.

## b08 · price_level

Distinguish sequential rates from the accumulated price level.

**Cần thấy:** The same loaf moves20,000→22,000→22,440; the10% and2% slopes differ while the level never falls.

**Mở cảnh:** A continuous price-height track with three equal-duration periods and one fixed bread silhouette/photo.

- “Từ hai mươi lên hai mươi hai nghìn” → Move the loaf/price marker up from20,000 to22,000; label +10%. → First increase is complete.
- “Nếu kỳ sau chỉ tăng hai phần trăm” → Continue a smaller positive rise; change the rate, not the baseline. → Second increment is applied to22,000.
- “hai mươi hai nghìn bốn trăm bốn mươi” → Land exactly on22,440, leaving20,000 as reference. → A smaller positive rate produces a still-higher level.

**Phạm vi:** Phép tính minh họa · không phải CPI

**Dữ liệu:** {"prices": [20000, 22000, 22440], "ratesPercent": [10, 2], "periods": ["Mốc đầu", "Kỳ1", "Kỳ2"], "sameQuantityQuality": true}

- Tránh: Do not slope down on2%.
- Tránh: Do not use the22,440 price in the later same-period wage calculation.

## b09 · price_level

Make the two meanings of down/up visible together.

**Cần thấy:** Rate contracts10%→2%; price remains20,000<22,000<22,440, without a misleading shared axis.

**Mở cảnh:** Keep the established price track; a separately labeled rate indicator is tied to each segment.

- “Tỷ lệ đã hạ từ mười xuống hai.” → Rate indicator shrinks10→2. → A slower pace is seen.
- “Số tiền phải trả vẫn tăng.” → Follow the price marker upward to22,440. → The price level keeps rising.
- “Hai việc ấy khác nhau.” → Contrast a smaller upward step with an actual downward step drawn only as a rejected expectation. → Viewer can distinguish disinflation from a price fall.

**Phạm vi:** Ví dụ minh họa · mức giá và tốc độ là hai đại lượng

**Dữ liệu:** {"prices": [20000, 22000, 22440], "ratesPercent": [10, 2]}

- Tránh: No dual-axis chart with unlabeled units.
- Tránh: Do not introduce deflation statistics.

## b10 · basket_scope

Show the limit of the bread example, then return to the exact arithmetic.

**Cần thấy:** One bread is a small member of a wider basket; other categories do not get invented weights or prices.

**Mở cảnh:** Begin with the same bread used in b08, not a new food example.

- “Một ổ bánh không đại diện cho lạm phát cả nước.” → Camera pulls back to show bread among rent/transport/food/service objects. → Bread-only example is visibly a subset.
- “một rổ nhiều hàng hóa và dịch vụ” → Objects occupy qualitative positions with no pie percentages. → Scope broadens without creating a new numerical model.
- “nó cộng lên phần giá đã tăng từ trước” → Return to the original bread track and add the new increment on its previous endpoint. → The conceptual scope note reinforces the same spine.

**Phạm vi:** Minh họa phạm vi · không phải quyền số CPI

**Dữ liệu:** {"categories": ["thực phẩm", "nhà ở", "đi lại", "dịch vụ"], "weights": null}

- Tránh: No100-part basket or invented inflation contribution.

## b11 · inventory

Turn a headline rate into the concrete invoice question.

**Cần thấy:** A lower reported rate does not erase dated receipts; a genuinely lower new flour invoice is a distinct event.

**Mở cảnh:** Existing receipt/lease/electricity papers remain unchanged around one flour sack.

- “tự suy ra bao bột, tiền thuê và tiền điện của mình đã về giá cũ” → A generic smaller-rate marker moves past dated documents without changing their amounts. → Macro rate does not automatically rewrite individual costs.
- “một hóa đơn thực sự giảm” → A new flour invoice is visibly replaced by a lower qualitative cost state. → Now the input really has changed.
- “khách có được chờ bánh rẻ lại không?” → Follow the invoice toward the same bread price, stopping before changing it. → Cause and possible pass-through remain to be explained.

**Phạm vi:** Tình huống giả định · chưa có mức giảm cụ thể

**Dữ liệu:** {"newFlourCostDirection": "lower", "actualAmount": null}

- Tránh: No fabricated numeric flour price or current headline.

## b12 · inventory

Explain possible timing lag by tracing the sack used in today’s batch.

**Cần thấy:** Old high-cost flour feeds today’s bread while a newly cheaper sack is still in stock.

**Mở cảnh:** A shelf contains one dated old lot and a newly arrived lot; the production path starts at the old lot.

- “lô mua trước, giá cao” → Highlight old dated sack and its invoice; route flour into the current batch. → Today’s cost follows the actual lot being used.
- “Hóa đơn mới thấp hơn” → Place the new cheaper sack in the receiving area, keeping it out of today’s batch. → A newer invoice exists without changing the current input lot.
- “một độ trễ có thể có” → Advance the new sack only into a later batch, with a possible marker. → The lag is a conditional process, not a permanent excuse.

**Phạm vi:** Một khả năng minh họa · không áp dụng mọi tiệm

**Dữ liệu:** {"lots": ["Lô trước", "Lô mới"], "costDirections": ["cao hơn", "thấp hơn"], "numericalCosts": null}

- Tránh: Do not assert FIFO accounting is mandatory or every shop uses old stock.
- Tránh: No stock bobbing without actual lot-to-batch movement.

## b13 · cost_ledger

Make one decreasing component different from the total.

**Cần thấy:** Flour decreases; lease/wage commitments persist; remaining ingredients/energy can move separately.

**Mở cảnh:** A ledger assembled from actual expense objects; only flour is selected initially.

- “Tiền thuê vẫn theo hợp đồng.” → The rent document stays locked in place while flour shrinks. → Some costs do not move with the newest flour invoice.
- “Lương người phụ bán đã thỏa thuận.” → Wage commitment remains, distinct from the later hypothetical wage comparison. → Another retained cost component is visible.
- “Một dòng giảm chưa có nghĩa tổng chi phí” → Route all expense lines into a total bracket while changing only the flour line. → The sign of the total cannot be inferred from a single line.

**Phạm vi:** Minh họa quan hệ chi phí · không có mức giá thị trường

**Dữ liệu:** {"items": ["bột", "thuê", "lương", "điện", "nhân", "bao bì"], "numericValues": null, "qualitativeStates": true}

- Tránh: Do not invent equal weights for costs or a numeric total.
- Tránh: Do not crowd six full text cards around the footage.

## b14 · cost_ledger

Test the explanation with an explicit counterexample.

**Cần thấy:** Total costs really fall, sales quantity and selling price stay unchanged, so the remainder can expand.

**Mở cảnh:** The same shop ledger; now every necessary assumption is visibly pinned before the cost change.

- “nếu tổng chi phí đã giảm thật” → Shrink the whole cost requirement, not just the flour piece. → This counterfactual differs from b13.
- “lượng bán vẫn như cũ” → Keep the number of breads/payments unchanged. → Volume is held constant.
- “chị Hạnh giữ giá” → The selling-price marker stays fixed. → Revenue per bread stays fixed.
- “Khoảng dư có thể tăng.” → Release the space previously occupied by cost into the remainder. → A conditional larger remainder is the outcome.

**Phạm vi:** Phản ví dụ có điều kiện · chưa phải lãi ròng

**Dữ liệu:** {"sellingPrice": "unchanged", "salesVolume": "unchanged", "totalCost": "decreases", "remainder": "can_increase", "newNumericAmounts": null}

- Tránh: Do not show a tax/depreciation-adjusted net profit.
- Tránh: Do not repeat b05 and imply costs rose in this counterexample.

## b15 · competition

Give the buyer a meaningful decision rather than decorative people.

**Cần thấy:** Two comparable breads, accessible alternative, customer choice and a possible loss of orders at the higher-price shop.

**Mở cảnh:** Two actual shop windows/bread images, linked by a walkable qualitative route; a customer is represented by an order token, not a cartoon presenter.

- “bánh tương đương, rẻ hơn và dễ mua” → Open a route to comparable bread with a lower relative tag, no invented new numeric price. → Switching is feasible.
- “cân nhắc mất khách” → Order tokens turn toward the alternative; original shop has fewer arriving orders. → Competition changes the shop’s incentive.
- “khách khó chuyển chỗ mua” → Show the same route as obstructed/inconvenient in a second conditional state. → Switching pressure becomes weaker.
- “không chỉ phép cộng trên hóa đơn” → Rejoin the invoice decision with the customer-choice route. → Price-setting has both cost and demand conditions.

**Phạm vi:** Minh họa lựa chọn · không phải dữ liệu thị phần

**Dữ liệu:** {"comparison": "same_quantity_quality", "alternative": "relatively_cheaper_accessible", "marketShareNumbers": null}

- Tránh: No invented customer counts/percent market share presented as measured.
- Tránh: No cash/coin rain as generic success.

## b16 · real footage

Create a visual handoff from the counter to the buyer’s wallet.

**Cần thấy:** A real transaction ends; receipt and purchase are now viewed from the buyer side.

**Mở cảnh:** Actual counter/payment action with the bread visible, not another oven shot.

- “tổng chi phí đã đổi bao nhiêu” → Receipt side remains in view long enough to recall the cost question. → Question one is anchored.
- “khách có lựa chọn nào?” → Reveal nearby shop/customer decision context. → Question two has an object.
- “chiếc ví của người mua” → A hand opens wallet/pay envelope, leading into income. → Camera follows the reasoning to the next viewpoint.

**Phạm vi:** Footage bối cảnh · không gắn danh tính hư cấu

**Dữ liệu:** {}

- Tránh: Do not assert an actual shopper’s salary or hardship.

## b17 · bread_power

Reset the period explicitly and compare the unequal growth rates.

**Cần thấy:** Use original20,000→22,000 price period, then income10,000,000→10,500,000; price+10% versus income+5%.

**Mở cảnh:** The price-level track returns visibly to its first two nodes; the22,440 next-period node withdraws before wages appear.

- “đúng kỳ chiếc bánh tăng từ hai mươi lên hai mươi hai nghìn” → Select only the original price period. → No accidental use of the later22,440 price.
- “từ mười triệu lên mười triệu rưỡi” → A pay envelope grows10m→10.5m. → Nominal income rises5%.
- “giá bữa sáng đã tăng nhanh hơn lương” → Compare the +10% price increment to the +5% income increment, with units explicit. → The mismatch is seen before dividing quantities.

**Phạm vi:** Thu nhập/giá giả định · cùng kỳ20.000→22.000

**Dữ liệu:** {"priceBefore": 20000, "priceAfter": 22000, "incomeBefore": 10000000, "incomeAfter": 10500000, "priceRate": 10, "incomeRate": 5}

- Tránh: No fake wage slip representing a real stock employee.

## b18 · bread_power

Transform income into a same-product purchasing-power yardstick.

**Cần thấy:** 10m÷20k=500 bread-equivalent units;10.5m÷22k≈477.3; quantity and quality stay the same.

**Mở cảnh:** A measuring rack/grid represents bread-equivalent capacity, with a legend that groups are schematic, not actual loaves bought.

- “Mười triệu tương đương năm trăm ổ giá cũ.” → The old income fills the capacity grid to500 at20k/unit. → Baseline quantity is established.
- “khoảng bốn trăm bảy mươi bảy ổ giá mới” → Apply10.5m/22k and withdraw22.7 bread-equivalent capacity. → Higher income buys fewer same-type units.
- “Không ai cần đem toàn bộ lương đi mua bánh.” → The rack becomes an explicit measuring scale rather than a literal shopping cart or monthly diet. → Viewer sees a ratio, not an assumed household budget.
- “thu nhập mỗi kỳ đổi được bao nhiêu” → Pin both divisions in compact sequential notation. → The changed capacity has a transparent calculation.

**Phạm vi:** Thước đo riêng bằng bánh · không giả định tiêu hết lương

**Dữ liệu:** {"before": 500, "after": 477.272727, "quantityDifference": -22.727273, "formulas": ["10.000.000/20.000=500", "10.500.000/22.000≈477,3"]}

- Tránh: Do not imply the worker buys500 loaves a month.
- Tránh: Do not show477 individual icons when unreadable; group with explicit scale.

## b19 · bread_power

Tie both sides of the same counter back together.

**Cần thấy:** Bread-equivalent purchasing power fallsabout4.5%; seller remainder3,000→2,500 is a different measure and not4.5%.

**Mở cảnh:** Keep the wage/bread ratio result; the original counter route can return as a spatial callback.

- “giảm khoảng bốn phẩy năm phần trăm” → Show (477.27/500−1)×100≈−4.5% attached only to bread purchasing power. → Correct relative change is explicit.
- “Nhìn từ quầy bán” → Restore3,000→2,500 with its own label/unit. → Seller result is recalled without mixing percentages.
- “Nhìn từ người làm công” → Return to500→477.3 capacity on the opposite side. → Two pressures coexist around one bread and one price change.

**Phạm vi:** Hai thước đo khác nhau · cùng ví dụ

**Dữ liệu:** {"breadPowerChangePercent": -4.5454545, "sellerRemainders": [3000, 2500], "breadQuantities": [500, 477.272727]}

- Tránh: Do not apply−4.5% to shop profit or national real wages.

## b20 · basket_scope

Expand scope without starting a second arithmetic story.

**Cần thấy:** Bread joins rent, transport and other spending categories; same quantities/quality are paired across time.

**Mở cảnh:** The bread yardstick is visible within a larger qualitative household basket.

- “Đời sống thật không chỉ có bánh mì.” → Pull back to show other spending objects. → The bread-only limitation is immediately visible.
- “cùng một giỏ chi tiêu với lượng và chất lượng tương đương” → Pair before/after baskets with identical objects and quantities; leave all prices blank. → Fair comparison requires a consistent basket.
- “không phải chiếc máy đo toàn bộ đời sống” → Keep the bread measure as a labeled subset. → No new CPI or household inflation number has been invented.

**Phạm vi:** Minh họa phạm vi · không tính giỏ hộ thực tế

**Dữ liệu:** {"categories": ["bánh/thực phẩm", "nhà ở", "đi lại", "khác"], "weights": null, "newPrices": null}

- Tránh: No100-unit allocation/pie or fabricated household shares.

## b21 · basket_scope

Explain why experiences can differ from an average.

**Cần thấy:** Two qualitative baskets emphasize different items; the item that grows in cost is more important to one basket than another.

**Mở cảnh:** Reuse b20 objects, arrange them differently without fixed percentages.

- “những khoản anh mua nhiều tăng nhanh” → Highlight the frequently bought category and a relative cost pressure marker. → Exposure depends on what the person buys.
- “Nhà khác chi tiêu khác” → Shift attention to another qualitative basket with a different emphasized item. → Different experiences need not contradict a common aggregate.
- “không tự chứng minh bản tin sai” → Bring the average concept and personal basket into distinct labeled scopes. → The film avoids declaring either subjective or aggregate experience invalid.

**Phạm vi:** Minh họa khác biệt cơ cấu chi tiêu

**Dữ liệu:** {"weights": "qualitative_only", "aggregateNumbers": null}

- Tránh: Do not imply exact national weights or calculate personal inflation from invented shares.

## b22 · synthesis

Resolve the hook with three previously proven relations.

**Cần thấy:** Price-versus-cost, rate-versus-level, wage-versus-bread capacity return in spoken order around the same bread.

**Mở cảnh:** A continuous counter/receipt path recalls the opening; only one relation is active at a time.

- “Khách trả thêm hai nghìn không có nghĩa chị giữ thêm hai nghìn.” → Follow2,000 toward the larger2,500 extra cost. → Seller outcome recalls its causal proof.
- “Tin lạm phát giảm không có nghĩa giá trở lại mốc cũ.” → Transform the route into the rising price track with smaller second step. → Rate/level distinction returns.
- “lương tăng không tự bảo đảm mua được nhiều hơn” → Transform to10m/20k versus10.5m/22k capacity. → Purchasing-power result returns.
- “Ba điều ấy có thể cùng đúng” → Bring the three end states into one connected scene, not three equal-size paragraph cards. → The opening paradox is resolved.

**Phạm vi:** Tổng hợp chính ví dụ đã giải

**Dữ liệu:** {"priceIncrement": 2000, "costIncrement": 2500, "pricePath": [20000, 22000, 22440], "incomePath": [10000000, 10500000], "breadQuantityPath": [500, 477.272727]}

- Tránh: Do not repeat full narration as captions.
- Tránh: Do not introduce a fourth causal claim in the payoff.

## b23 · real footage

Return the lesson to an action the viewer can perform.

**Cần thấy:** Real breakfast purchase/receipt checked against an earlier dated equivalent and the person’s own income record; no asserted private figures.

**Mở cảnh:** Actual hands compare a price/receipt, with the bread in frame.

- “đang tăng chậm hơn hay giảm giá thật?” → Briefly activate the rate/level distinction next to the receipt. → First check is concrete.
- “So với mốc nào?” → Point to date/baseline, not a giant question card. → Second check is a comparison anchor.
- “cùng lượng, cùng chất lượng” → Align comparable bread portions before returning clean footage. → Third check is comparability, not merely a numerical headline.

**Phạm vi:** Bối cảnh minh họa · kiểm mốc/lượng/chất lượng

**Dữ liệu:** {}

- Tránh: No fake banking salary screen or unrelated investment imagery.

## b24 · real footage

Invite a meaningful example and finish the bread callback.

**Cần thấy:** Actual bread preparation/purchase resolves; one concise interaction cue can accompany the spoken request.

**Mở cảnh:** Warm real finished-bread handoff or a person choosing breakfast, without assigning a fictional identity.

- “bạn đang so với năm nào?” → Show a small comparison-year prompt next to the same bread. → Comment request carries the baseline habit.
- “hãy đăng ký kênh và bật chuông” → One restrained subscribe/bell action, then return to finished bread. → The film ends on its subject, not a page of interface text.

**Phạm vi:** Không branding tự đặt

**Dữ liệu:** {}

- Tránh: No invented channel name.
- Tránh: No repeated CTA cards/subtitles.

## Kiểm đa dạng thực chất

- Relabeled static cards: Money physically routes/splits; price travels through time; inventory feeds a batch; ledger aggregates; order token chooses; income divides into capacity; basket changes scope; synthesis morphs previously proven relations.
- Every unit repeats the same reveal/hold: Use the final state of one unit as the starting state of the next; b05 adds a counterfactual and decision, b06 traces the increment rather than replaying the whole sum.
- Background footage is just decoration: Use real interludes b02,b07,b16,b23,b24 for actual object/action viewpoint changes; leave the calculation scene while it has an explanatory job.
- More information becomes unreadable: Present labels and figures in the spoken order, retire no-longer-needed figures, keep model scope readable; never copy the paragraph as on-screen text.
- Eighteen simulations imply one acceptable style: Inspect full moving sequences b03–b06, b11–b15, b17–b19 and b22 before the full render; count/family names and technical passes do not establish variety.
