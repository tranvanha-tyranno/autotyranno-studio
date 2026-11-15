"""Write the clause-level semantic design for the simulation/OpenAI revision.

This creates an editorial plan, not rendered-motion or aesthetic approval.
"""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]
BATCH = ROOT / 'videos/2026-11-15-banh-mi-mo-phong-openai'


def stage(cue, action, state):
    return {'spokenPhrase': cue, 'action': action, 'changedState': state}


def row(uid, family, role, need, setup, stages, values=None, scope='Ví dụ minh họa', interlude=None, avoid=None):
    return {'unitId': uid, 'family': family, 'mode': 'simulation' if family else 'real_footage',
            'storyFunction': role, 'whatMustBeVisible': need, 'setup': setup, 'stages': stages,
            'data': values or {}, 'scopeLabel': scope, 'realFootageInterlude': interlude,
            'avoid': avoid or []}


ROWS = [
 row('b01','money_split','Visualize the opening paradox before explaining it.',
     'The same loaf has price+2,000 while the shop remainder falls500; the two arrows must not imply aggregate national outcomes.',
     'One bread on an actual counter; two money routes are still connected to that same bread.',[
     stage('Ổ bánh tăng hai nghìn.','The price tag changes20,000→22,000 and the extra2,000 travels out of the buyer side.','Customer outlay rises2,000.'),
     stage('người bán lại giữ được ít hơn năm trăm đồng','The seller remainder changes3,000→2,500 and a500 difference leaves the remainder.','Customer outlay and seller retained amount move in opposite directions.'),
     stage('Vì sao cả hai vẫn thấy khó hơn?','Keep only the two conflicting outcomes and the same bread, opening the unanswered route between them.','A concrete unresolved relation, not a title card.')],
     {'priceBefore':20000,'priceAfter':22000,'remainderBefore':3000,'remainderAfter':2500,'difference':-500},
     avoid=['Do not call the remainder net profit.','Do not display all future wage/CPI information in the hook.']),
 row('b02',None,'Orient the single bakery story and plant the three objects that will return.',
     'Real hands prepare one consistent bread type; price board, receipt and pay envelope become three distinct points of inquiry.',
     'Actual bakery preparation; footage people remain unnamed illustrative people.',[
     stage('tiệm bánh giả định của chị Hạnh','Use a short in-scene hypothetical label without a disclaimer screen.','Scope established inside the story.'),
     stage('bảng giá, hóa đơn đầu vào, và tiền người mua kiếm được','Briefly show the corresponding three objects in that spoken order.','Three concrete objects, not three abstract dashboard cards.')],
     scope='Tiệm giả định; footage là bối cảnh',avoid=['Never identify stock staff as Hạnh or claim their real finances.']),
 row('b03','money_split','Make the baseline arithmetic spatial and causal.',
     '20,000 physically divides into12,000 variable costs,5,000 fixed allocation and3,000 remainder.',
     'An intact20,000 strip/stack enters at the payment point; one bread pins the unit of analysis.',[
     stage('một ổ bán hai mươi nghìn','Show the whole20,000 payment before splitting.','The viewer knows the total and unit.'),
     stage('hết mười hai nghìn','Route12,000 into ingredients/variable costs.','8,000 still unallocated.'),
     stage('được chia ra năm nghìn một ổ','Take5,000 into fixed allocation; the quantity/sales assumption stays pinned.','3,000 remains after the modeled costs.'),
     stage('Còn ba nghìn.','Isolate the physical3,000 remainder without a profit label.','Arithmetic has unfolded, not appeared as a completed table.')],
     {'price':20000,'variable':12000,'fixedAllocated':5000,'remainder':3000,'salesVolume':'held_constant_assumption'},
     scope='Ví dụ minh họa · cùng lượng bán giả định',avoid=['Do not show12k+5k+3k exceeding20k.','No continuously running counter after it reaches a meaningful state.']),
 row('b04','cost_ledger','Limit the interpretation of the preceding result.',
     '3,000 is an unfinished subtotal with tax, depreciation and owner labor not yet counted.',
     'Reuse the3,000 subtotal from b03; a real receipt or ledger surface supplies context.',[
     stage('Khoan gọi ba nghìn ấy là tiền bỏ túi.','Stop the3,000 moving toward an owner pocket; reopen it as an unfinished subtotal.','The remainder is explicitly provisional.'),
     stage('thuế, khấu hao và công của chủ tiệm','Add three unpriced/unfilled ledger lines, not invented costs.','Viewer sees what the model excludes.'),
     stage('so trước với sau','Pin the same scope to both before/after states.','Comparison remains valid only within this limited model.')],
     {'subtotal':3000,'excludedUnpricedItems':['thuế','khấu hao','công chủ tiệm']},scope='Khoảng dư mô hình · chưa phải lợi nhuận ròng',
     avoid=['No invented numeric tax, depreciation or wages.','Do not make the exclusions smaller than can be read at phone size.']),
 row('b05','money_split','Show the pressure and the shop decision as separate states.',
     'First keep sale20,000 with cost14,500+5,000 to leave500; only then raise sale22,000 to leave2,500.',
     'Same bread and fixed allocation as b03; variable-cost route is ready to expand.',[
     stage('thành mười bốn nghìn năm trăm','Variable cost grows12,000→14,500 while sale is still20,000.','Remainder shrinks3,000→500.'),
     stage('Nếu giữ giá cũ','Pause on the20,000 sale/500 remainder result.','The counterfactual is legible before the decision.'),
     stage('đổi bảng lên hai mươi hai nghìn','Sale changes20,000→22,000;2,000 refills part of the lost remainder.','Remainder recovers500→2,500 but remains below3,000.'),
     stage('đầu vào đã tăng hai nghìn năm trăm','Lay +2,000 received against +2,500 costs.','500 gap explains the paradox.')],
     {'oldPrice':20000,'newVariable':14500,'fixedAllocated':5000,'oldPriceRemainder':500,'newPrice':22000,'newRemainder':2500},
     scope='Ví dụ minh họa · cùng lượng bán giả định',avoid=['Do not reveal2,500 before narration says price is raised.']),
 row('b06','money_split','Prove the destination of the extra payment.',
     'A2,000 increment enters the expanded cost stream but cannot fill the whole2,500 expansion.',
     'Keep b05 routes and visually follow only the incremental money.',[
     stage('từ ba nghìn, tiệm chỉ còn hai nghìn năm trăm','Before/after remainders align to the same baseline.','A500 shortfall is seen directly.'),
     stage('Hai nghìn tăng thêm không biến mất.','The highlighted2,000 travels visibly into the2,500 extra-cost requirement.','The money has an explained destination.'),
     stage('Nó chưa bù hết phần chi phí tăng.','Leave the500 uncovered notch in the extra-cost route.','The explanatory result appears as a physical gap, not a slogan.')],
     {'saleIncrement':2000,'costIncrement':2500,'uncoveredIncrement':500,'remainders':[3000,2500]},
     scope='Ví dụ minh họa · khoản dư, chưa phải lãi ròng',interlude='Return to a real receipt/ingredient action once the incremental route is understood.',
     avoid=['Do not repeat the entire baseline calculation from zero.']),
 row('b07',None,'Release the graphic and ask the next unresolved question.',
     'Actual bread purchase, then the existing22,000 price board; alternative shop outcomes must be framed as possibilities.',
     'Real hand-to-counter transaction or bread finishing, without invented identities.',[
     stage('muốn kết luận phải có sổ thật','The illustrative ledger withdraws; real-world context is shown without asserting a particular shop outcome.','Scope of inference is clear.'),
     stage('tại sao bảng giá không quay về hai mươi nghìn?','A20,000 reference mark appears beside the present22,000 label without resetting it.','The new question is rate versus level.')],scope='Bối cảnh minh họa',avoid=['Do not fabricate news screenshots or current official inflation numbers.']),
 row('b08','price_level','Distinguish sequential rates from the accumulated price level.',
     'The same loaf moves20,000→22,000→22,440; the10% and2% slopes differ while the level never falls.',
     'A continuous price-height track with three equal-duration periods and one fixed bread silhouette/photo.',[
     stage('Từ hai mươi lên hai mươi hai nghìn','Move the loaf/price marker up from20,000 to22,000; label +10%.','First increase is complete.'),
     stage('Nếu kỳ sau chỉ tăng hai phần trăm','Continue a smaller positive rise; change the rate, not the baseline.','Second increment is applied to22,000.'),
     stage('hai mươi hai nghìn bốn trăm bốn mươi','Land exactly on22,440, leaving20,000 as reference.','A smaller positive rate produces a still-higher level.')],
     {'prices':[20000,22000,22440],'ratesPercent':[10,2],'periods':['Mốc đầu','Kỳ1','Kỳ2'],'sameQuantityQuality':True},
     scope='Phép tính minh họa · không phải CPI',avoid=['Do not slope down on2%.','Do not use the22,440 price in the later same-period wage calculation.']),
 row('b09','price_level','Make the two meanings of down/up visible together.',
     'Rate contracts10%→2%; price remains20,000<22,000<22,440, without a misleading shared axis.',
     'Keep the established price track; a separately labeled rate indicator is tied to each segment.',[
     stage('Tỷ lệ đã hạ từ mười xuống hai.','Rate indicator shrinks10→2.','A slower pace is seen.'),
     stage('Số tiền phải trả vẫn tăng.','Follow the price marker upward to22,440.','The price level keeps rising.'),
     stage('Hai việc ấy khác nhau.','Contrast a smaller upward step with an actual downward step drawn only as a rejected expectation.','Viewer can distinguish disinflation from a price fall.')],
     {'prices':[20000,22000,22440],'ratesPercent':[10,2]},scope='Ví dụ minh họa · mức giá và tốc độ là hai đại lượng',
     avoid=['No dual-axis chart with unlabeled units.','Do not introduce deflation statistics.']),
 row('b10','basket_scope','Show the limit of the bread example, then return to the exact arithmetic.',
     'One bread is a small member of a wider basket; other categories do not get invented weights or prices.',
     'Begin with the same bread used in b08, not a new food example.',[
     stage('Một ổ bánh không đại diện cho lạm phát cả nước.','Camera pulls back to show bread among rent/transport/food/service objects.','Bread-only example is visibly a subset.'),
     stage('một rổ nhiều hàng hóa và dịch vụ','Objects occupy qualitative positions with no pie percentages.','Scope broadens without creating a new numerical model.'),
     stage('nó cộng lên phần giá đã tăng từ trước','Return to the original bread track and add the new increment on its previous endpoint.','The conceptual scope note reinforces the same spine.')],
     {'categories':['thực phẩm','nhà ở','đi lại','dịch vụ'],'weights':None},scope='Minh họa phạm vi · không phải quyền số CPI',
     avoid=['No100-part basket or invented inflation contribution.']),
 row('b11','inventory','Turn a headline rate into the concrete invoice question.',
     'A lower reported rate does not erase dated receipts; a genuinely lower new flour invoice is a distinct event.',
     'Existing receipt/lease/electricity papers remain unchanged around one flour sack.',[
     stage('tự suy ra bao bột, tiền thuê và tiền điện của mình đã về giá cũ','A generic smaller-rate marker moves past dated documents without changing their amounts.','Macro rate does not automatically rewrite individual costs.'),
     stage('một hóa đơn thực sự giảm','A new flour invoice is visibly replaced by a lower qualitative cost state.','Now the input really has changed.'),
     stage('khách có được chờ bánh rẻ lại không?','Follow the invoice toward the same bread price, stopping before changing it.','Cause and possible pass-through remain to be explained.')],
     {'newFlourCostDirection':'lower','actualAmount':None},scope='Tình huống giả định · chưa có mức giảm cụ thể',
     avoid=['No fabricated numeric flour price or current headline.']),
 row('b12','inventory','Explain possible timing lag by tracing the sack used in today’s batch.',
     'Old high-cost flour feeds today’s bread while a newly cheaper sack is still in stock.',
     'A shelf contains one dated old lot and a newly arrived lot; the production path starts at the old lot.',[
     stage('lô mua trước, giá cao','Highlight old dated sack and its invoice; route flour into the current batch.','Today’s cost follows the actual lot being used.'),
     stage('Hóa đơn mới thấp hơn','Place the new cheaper sack in the receiving area, keeping it out of today’s batch.','A newer invoice exists without changing the current input lot.'),
     stage('một độ trễ có thể có','Advance the new sack only into a later batch, with a possible marker.','The lag is a conditional process, not a permanent excuse.')],
     {'lots':['Lô trước','Lô mới'],'costDirections':['cao hơn','thấp hơn'],'numericalCosts':None},scope='Một khả năng minh họa · không áp dụng mọi tiệm',
     avoid=['Do not assert FIFO accounting is mandatory or every shop uses old stock.','No stock bobbing without actual lot-to-batch movement.']),
 row('b13','cost_ledger','Make one decreasing component different from the total.',
     'Flour decreases; lease/wage commitments persist; remaining ingredients/energy can move separately.',
     'A ledger assembled from actual expense objects; only flour is selected initially.',[
     stage('Tiền thuê vẫn theo hợp đồng.','The rent document stays locked in place while flour shrinks.','Some costs do not move with the newest flour invoice.'),
     stage('Lương người phụ bán đã thỏa thuận.','Wage commitment remains, distinct from the later hypothetical wage comparison.','Another retained cost component is visible.'),
     stage('Một dòng giảm chưa có nghĩa tổng chi phí','Route all expense lines into a total bracket while changing only the flour line.','The sign of the total cannot be inferred from a single line.')],
     {'items':['bột','thuê','lương','điện','nhân','bao bì'],'numericValues':None,'qualitativeStates':True},scope='Minh họa quan hệ chi phí · không có mức giá thị trường',
     avoid=['Do not invent equal weights for costs or a numeric total.','Do not crowd six full text cards around the footage.']),
 row('b14','cost_ledger','Test the explanation with an explicit counterexample.',
     'Total costs really fall, sales quantity and selling price stay unchanged, so the remainder can expand.',
     'The same shop ledger; now every necessary assumption is visibly pinned before the cost change.',[
     stage('nếu tổng chi phí đã giảm thật','Shrink the whole cost requirement, not just the flour piece.','This counterfactual differs from b13.'),
     stage('lượng bán vẫn như cũ','Keep the number of breads/payments unchanged.','Volume is held constant.'),
     stage('chị Hạnh giữ giá','The selling-price marker stays fixed.','Revenue per bread stays fixed.'),
     stage('Khoảng dư có thể tăng.','Release the space previously occupied by cost into the remainder.','A conditional larger remainder is the outcome.')],
     {'sellingPrice':'unchanged','salesVolume':'unchanged','totalCost':'decreases','remainder':'can_increase','newNumericAmounts':None},scope='Phản ví dụ có điều kiện · chưa phải lãi ròng',
     avoid=['Do not show a tax/depreciation-adjusted net profit.','Do not repeat b05 and imply costs rose in this counterexample.']),
 row('b15','competition','Give the buyer a meaningful decision rather than decorative people.',
     'Two comparable breads, accessible alternative, customer choice and a possible loss of orders at the higher-price shop.',
     'Two actual shop windows/bread images, linked by a walkable qualitative route; a customer is represented by an order token, not a cartoon presenter.',[
     stage('bánh tương đương, rẻ hơn và dễ mua','Open a route to comparable bread with a lower relative tag, no invented new numeric price.','Switching is feasible.'),
     stage('cân nhắc mất khách','Order tokens turn toward the alternative; original shop has fewer arriving orders.','Competition changes the shop’s incentive.'),
     stage('khách khó chuyển chỗ mua','Show the same route as obstructed/inconvenient in a second conditional state.','Switching pressure becomes weaker.'),
     stage('không chỉ phép cộng trên hóa đơn','Rejoin the invoice decision with the customer-choice route.','Price-setting has both cost and demand conditions.')],
     {'comparison':'same_quantity_quality','alternative':'relatively_cheaper_accessible','marketShareNumbers':None},scope='Minh họa lựa chọn · không phải dữ liệu thị phần',
     avoid=['No invented customer counts/percent market share presented as measured.','No cash/coin rain as generic success.']),
 row('b16',None,'Create a visual handoff from the counter to the buyer’s wallet.',
     'A real transaction ends; receipt and purchase are now viewed from the buyer side.',
     'Actual counter/payment action with the bread visible, not another oven shot.',[
     stage('tổng chi phí đã đổi bao nhiêu','Receipt side remains in view long enough to recall the cost question.','Question one is anchored.'),
     stage('khách có lựa chọn nào?','Reveal nearby shop/customer decision context.','Question two has an object.'),
     stage('chiếc ví của người mua','A hand opens wallet/pay envelope, leading into income.','Camera follows the reasoning to the next viewpoint.')],scope='Footage bối cảnh · không gắn danh tính hư cấu',avoid=['Do not assert an actual shopper’s salary or hardship.']),
 row('b17','bread_power','Reset the period explicitly and compare the unequal growth rates.',
     'Use original20,000→22,000 price period, then income10,000,000→10,500,000; price+10% versus income+5%.',
     'The price-level track returns visibly to its first two nodes; the22,440 next-period node withdraws before wages appear.',[
     stage('đúng kỳ chiếc bánh tăng từ hai mươi lên hai mươi hai nghìn','Select only the original price period.','No accidental use of the later22,440 price.'),
     stage('từ mười triệu lên mười triệu rưỡi','A pay envelope grows10m→10.5m.','Nominal income rises5%.'),
     stage('giá bữa sáng đã tăng nhanh hơn lương','Compare the +10% price increment to the +5% income increment, with units explicit.','The mismatch is seen before dividing quantities.')],
     {'priceBefore':20000,'priceAfter':22000,'incomeBefore':10000000,'incomeAfter':10500000,'priceRate':10,'incomeRate':5},scope='Thu nhập/giá giả định · cùng kỳ20.000→22.000',avoid=['No fake wage slip representing a real stock employee.']),
 row('b18','bread_power','Transform income into a same-product purchasing-power yardstick.',
     '10m÷20k=500 bread-equivalent units;10.5m÷22k≈477.3; quantity and quality stay the same.',
     'A measuring rack/grid represents bread-equivalent capacity, with a legend that groups are schematic, not actual loaves bought.',[
     stage('Mười triệu tương đương năm trăm ổ giá cũ.','The old income fills the capacity grid to500 at20k/unit.','Baseline quantity is established.'),
     stage('khoảng bốn trăm bảy mươi bảy ổ giá mới','Apply10.5m/22k and withdraw22.7 bread-equivalent capacity.','Higher income buys fewer same-type units.'),
     stage('Không ai cần đem toàn bộ lương đi mua bánh.','The rack becomes an explicit measuring scale rather than a literal shopping cart or monthly diet.','Viewer sees a ratio, not an assumed household budget.'),
     stage('thu nhập mỗi kỳ đổi được bao nhiêu','Pin both divisions in compact sequential notation.','The changed capacity has a transparent calculation.')],
     {'before':500,'after':477.272727,'quantityDifference':-22.727273,'formulas':['10.000.000/20.000=500','10.500.000/22.000≈477,3']},scope='Thước đo riêng bằng bánh · không giả định tiêu hết lương',avoid=['Do not imply the worker buys500 loaves a month.','Do not show477 individual icons when unreadable; group with explicit scale.']),
 row('b19','bread_power','Tie both sides of the same counter back together.',
     'Bread-equivalent purchasing power fallsabout4.5%; seller remainder3,000→2,500 is a different measure and not4.5%.',
     'Keep the wage/bread ratio result; the original counter route can return as a spatial callback.',[
     stage('giảm khoảng bốn phẩy năm phần trăm','Show (477.27/500−1)×100≈−4.5% attached only to bread purchasing power.','Correct relative change is explicit.'),
     stage('Nhìn từ quầy bán','Restore3,000→2,500 with its own label/unit.','Seller result is recalled without mixing percentages.'),
     stage('Nhìn từ người làm công','Return to500→477.3 capacity on the opposite side.','Two pressures coexist around one bread and one price change.')],
     {'breadPowerChangePercent':-4.5454545,'sellerRemainders':[3000,2500],'breadQuantities':[500,477.272727]},scope='Hai thước đo khác nhau · cùng ví dụ',
     avoid=['Do not apply−4.5% to shop profit or national real wages.']),
 row('b20','basket_scope','Expand scope without starting a second arithmetic story.',
     'Bread joins rent, transport and other spending categories; same quantities/quality are paired across time.',
     'The bread yardstick is visible within a larger qualitative household basket.',[
     stage('Đời sống thật không chỉ có bánh mì.','Pull back to show other spending objects.','The bread-only limitation is immediately visible.'),
     stage('cùng một giỏ chi tiêu với lượng và chất lượng tương đương','Pair before/after baskets with identical objects and quantities; leave all prices blank.','Fair comparison requires a consistent basket.'),
     stage('không phải chiếc máy đo toàn bộ đời sống','Keep the bread measure as a labeled subset.','No new CPI or household inflation number has been invented.')],
     {'categories':['bánh/thực phẩm','nhà ở','đi lại','khác'],'weights':None,'newPrices':None},scope='Minh họa phạm vi · không tính giỏ hộ thực tế',avoid=['No100-unit allocation/pie or fabricated household shares.']),
 row('b21','basket_scope','Explain why experiences can differ from an average.',
     'Two qualitative baskets emphasize different items; the item that grows in cost is more important to one basket than another.',
     'Reuse b20 objects, arrange them differently without fixed percentages.',[
     stage('những khoản anh mua nhiều tăng nhanh','Highlight the frequently bought category and a relative cost pressure marker.','Exposure depends on what the person buys.'),
     stage('Nhà khác chi tiêu khác','Shift attention to another qualitative basket with a different emphasized item.','Different experiences need not contradict a common aggregate.'),
     stage('không tự chứng minh bản tin sai','Bring the average concept and personal basket into distinct labeled scopes.','The film avoids declaring either subjective or aggregate experience invalid.')],
     {'weights':'qualitative_only','aggregateNumbers':None},scope='Minh họa khác biệt cơ cấu chi tiêu',avoid=['Do not imply exact national weights or calculate personal inflation from invented shares.']),
 row('b22','synthesis','Resolve the hook with three previously proven relations.',
     'Price-versus-cost, rate-versus-level, wage-versus-bread capacity return in spoken order around the same bread.',
     'A continuous counter/receipt path recalls the opening; only one relation is active at a time.',[
     stage('Khách trả thêm hai nghìn không có nghĩa chị giữ thêm hai nghìn.','Follow2,000 toward the larger2,500 extra cost.','Seller outcome recalls its causal proof.'),
     stage('Tin lạm phát giảm không có nghĩa giá trở lại mốc cũ.','Transform the route into the rising price track with smaller second step.','Rate/level distinction returns.'),
     stage('lương tăng không tự bảo đảm mua được nhiều hơn','Transform to10m/20k versus10.5m/22k capacity.','Purchasing-power result returns.'),
     stage('Ba điều ấy có thể cùng đúng','Bring the three end states into one connected scene, not three equal-size paragraph cards.','The opening paradox is resolved.')],
     {'priceIncrement':2000,'costIncrement':2500,'pricePath':[20000,22000,22440],'incomePath':[10000000,10500000],'breadQuantityPath':[500,477.272727]},scope='Tổng hợp chính ví dụ đã giải',
     avoid=['Do not repeat full narration as captions.','Do not introduce a fourth causal claim in the payoff.']),
 row('b23',None,'Return the lesson to an action the viewer can perform.',
     'Real breakfast purchase/receipt checked against an earlier dated equivalent and the person’s own income record; no asserted private figures.',
     'Actual hands compare a price/receipt, with the bread in frame.',[
     stage('đang tăng chậm hơn hay giảm giá thật?','Briefly activate the rate/level distinction next to the receipt.','First check is concrete.'),
     stage('So với mốc nào?','Point to date/baseline, not a giant question card.','Second check is a comparison anchor.'),
     stage('cùng lượng, cùng chất lượng','Align comparable bread portions before returning clean footage.','Third check is comparability, not merely a numerical headline.')],scope='Bối cảnh minh họa · kiểm mốc/lượng/chất lượng',avoid=['No fake banking salary screen or unrelated investment imagery.']),
 row('b24',None,'Invite a meaningful example and finish the bread callback.',
     'Actual bread preparation/purchase resolves; one concise interaction cue can accompany the spoken request.',
     'Warm real finished-bread handoff or a person choosing breakfast, without assigning a fictional identity.',[
     stage('bạn đang so với năm nào?','Show a small comparison-year prompt next to the same bread.','Comment request carries the baseline habit.'),
     stage('hãy đăng ký kênh và bật chuông','One restrained subscribe/bell action, then return to finished bread.','The film ends on its subject, not a page of interface text.')],scope='Không branding tự đặt',avoid=['No invented channel name.','No repeated CTA cards/subtitles.'])
]


def main():
    from bread_documentary_content import CONTENT
    units=[u for c in CONTENT['chapters'] for u in c['units']]
    by_id={u['id']:u for u in units}
    assert [r['unitId'] for r in ROWS]==list(by_id)
    for r in ROWS:
        r['narration']=by_id[r['unitId']]['text']
        for s in r['stages']:
            if s['spokenPhrase'] not in r['narration']:
                raise ValueError('Cue is not exact script: '+r['unitId']+' '+s['spokenPhrase'])
    assert 20000-12000-5000==3000
    assert 20000-14500-5000==500
    assert 22000-14500-5000==2500
    assert round(22000*1.02)==22440
    ratio=(10500000/22000)/(10000000/20000)-1
    assert abs(ratio*100-(-4.545454545))<.00001
    result={'schema':'bread-simulation-editorial-plan/1','date':'2026-11-15',
      'status':'editorial design; not rendered QA or user approval',
      'scriptSource':'workflows/reference-video/bread_documentary_content.py',
      'scriptSHA256':hashlib.sha256(json.dumps(CONTENT,ensure_ascii=False,sort_keys=True).encode()).hexdigest(),
      'counts':{'units':24,'simulationUnits':sum(r['mode']=='simulation' for r in ROWS),'realFootageUnits':sum(r['mode']=='real_footage' for r in ROWS)},
      'principles':['Information density means visible relations, states and consequences, not more sentences on screen.',
        'One active focal relation at a time; retain earlier state as a comparison anchor only when needed.',
        'Eight families must have different physical operations and compositions, not relabeled cards.',
        'Every animation must connect setup→operation→changed state at an exact narration cue.',
        'Same bread spine and financial assumptions persist. Stock context never identifies fictional people.',
        'Phrase cues are exact source text, not measured times. Align them to the new OpenAI take before rendering.'],
      'creativeDiversityReview':[
        {'risk':'Relabeled static cards','remedy':'Money physically routes/splits; price travels through time; inventory feeds a batch; ledger aggregates; order token chooses; income divides into capacity; basket changes scope; synthesis morphs previously proven relations.'},
        {'risk':'Every unit repeats the same reveal/hold','remedy':'Use the final state of one unit as the starting state of the next; b05 adds a counterfactual and decision, b06 traces the increment rather than replaying the whole sum.'},
        {'risk':'Background footage is just decoration','remedy':'Use real interludes b02,b07,b16,b23,b24 for actual object/action viewpoint changes; leave the calculation scene while it has an explanatory job.'},
        {'risk':'More information becomes unreadable','remedy':'Present labels and figures in the spoken order, retire no-longer-needed figures, keep model scope readable; never copy the paragraph as on-screen text.'},
        {'risk':'Eighteen simulations imply one acceptable style','remedy':'Inspect full moving sequences b03–b06, b11–b15, b17–b19 and b22 before the full render; count/family names and technical passes do not establish variety.'}],
      'mathAudit':{'costRemainders':[3000,500,2500],'netProfitClaim':False,'fixedAllocationAssumption':'same quantity sold;5,000perunit held fixed','pricePath':[20000,22000,22440],'wageOriginalPeriodOnly':[20000,22000],'breadQuantities':[500,477.2727272727],'breadPurchasingPowerPercent':ratio*100,'inventoryCompetition':'qualitative only; no market statistics','basket':'scope concept only; no new household numerical model'},
      'units':ROWS}
    out=BATCH/'research';out.mkdir(parents=True,exist_ok=True)
    (out/'simulation-editorial-plan.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    lines=['# Mô phỏng phải làm rõ điều gì — 24 đoạn','',
      'Thiết kế biên tập, chưa phải kiểm bản dựng. 19/24 đoạn có mô phỏng mang thông tin; 5 đoạn footage làm điểm chuyển/nghỉ có nội dung. Cues là câu nguyên script, phải gắn vào audio OpenAI mới.','',
      'Không tăng thông tin bằng cách dán thêm đoạn chữ. Mỗi cảnh có vật/đại lượng, thao tác và kết quả đổi. Không nhân vật hoạt hình, không subtitle, không giả mạo nguồn/branding.','']
    for r in ROWS:
        lines += [f"## {r['unitId']} · {r['family'] or 'real footage'}",'',r['storyFunction'],'',f"**Cần thấy:** {r['whatMustBeVisible']}",'',f"**Mở cảnh:** {r['setup']}",'']
        lines += [f"- “{s['spokenPhrase']}” → {s['action']} → {s['changedState']}" for s in r['stages']]
        lines += ['',f"**Phạm vi:** {r['scopeLabel']}",f"\n**Dữ liệu:** {json.dumps(r['data'],ensure_ascii=False)}",'']
        if r['realFootageInterlude']:lines += [f"Footage nối: {r['realFootageInterlude']}",'']
        lines += [f"- Tránh: {a}" for a in r['avoid']]+['']
    lines+=['## Kiểm đa dạng thực chất','']+[f"- {x['risk']}: {x['remedy']}" for x in result['creativeDiversityReview']]
    (out/'simulation-editorial-plan.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps(result['counts']))


if __name__=='__main__':main()
