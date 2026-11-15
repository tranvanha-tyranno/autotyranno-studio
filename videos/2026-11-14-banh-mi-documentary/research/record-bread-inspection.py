"""Record only frames actually opened by content_a; retain rejected candidates."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
path=ROOT/'research/footage-sources.json'
d=json.loads(path.read_text(encoding='utf-8'))
notes={
11265880:('Both hands shape a round dough piece on a flour-covered white worktop; flour and pressing action visible across seven actual source frames. No finished baguette in this clip.',['flour','ingredients','bakery'],[.2,12.5]),
11265881:('Hands fold and press dough on a heavily floured white worktop, dough changes from held piece to folded mass. Same set as11265880; avoid adjacent reuse.',['flour','bakery','bread'],[.2,22.0]),
7405932:('Rows of elongated baguette-shaped rolls bake behind oven glass; warm orange oven light, loaf surfaces change gradually. Low action: use brief oven/energy-cost context, not a long held shot.',['bread','bakery'],[.2,23.8]),
7405927:('Baker rolls and places long dough cylinders in a bakery tray. Forearms and hands visible; multiple formed baguette shapes. Strong process action.',['bread','bakery','flour'],[.15,8.6]),
8180413:('Hands fold and push bread dough on a wooden table; a scale and glass ingredient jars in background. Visible kneading state changes; generic home baking context.',['bread','bakery','flour','ingredients'],[.2,32.3]),
8180409:('Portrait view: hands lift, turn and knead one dough mass at white table. Same kitchen as8180413, but different framing; center crop must keep hands and dough, no claim these are fictional staff.',['bread','bakery','flour'],[.2,39.6]),
8530514:('Hands unwrap and break a long baguette at a green outdoor picnic, bread and basket visible. Supports bread handling/consumption only; not a Vietnamese shop or supplier.',['bread'],[.2,21.9]),
8540402:('Produce-stall vendor holds card terminal as shopper taps card and collects paper bag. Trees and western market setting visible, no Vietnamese location claim.',['payment','market','groceries'],[.2,16.2]),
4121751:('Supermarket checkout: shoppers pack paper bag and hold pineapple beside card terminal. Supports checkout/bagging, not fictional bakery.',['payment','shop','groceries'],[.2,13.9]),
7593795:('Seated people in business clothes count banknotes in an office. USD-like banknotes visible; not VND, no link to Hạnh or exact wage. Contextual general money only.',['payment'],[.2,25.5]),
7692777:('Hands count dollar bills with notebook and pencil on table, anonymous chest crop. General budgeting context; never label dollar bills Vietnamese đồng or her actual revenue.',['payment','receipt'],[.2,19.2]),
30329515:('Close-up real baguette sandwich assembled with pork, cucumber/herbs and seasoning, then wrapped/bagged. Strong authentic Bánh Mì visual. Source provides Vietnamese identification; pixels show actual baguette and filling. Does not identify Hạnh or prove price.',['bread','bakery','ingredients','shop'],[.1,20.1]),
31317451:('Glass street-food cabinet with short elongated golden baguettes and meat trays; gloved hand lifts a loaf, vendor preparing behind display. Strong finished-bread/shop visual.',['bread','bakery','shop','storage'],[.1,5.55]),
30042091:('Gloved hands chop roast pork with large knife on round wooden board and gather slices near containers. Ingredient preparation only, not finished bread, costs or hygiene conclusion.',['ingredients'],[.1,10.75]),
29980691:('Portrait close-up of black-gloved hands kneading a large dough mass in flour at commercial work surface. Dough rounds and folds; no pizza toppings visible. Generic dough-process context only.',['flour','bakery','bread'],[.2,38.3]),
13726352:('Portrait brick oven with bread shovel and thin flatbreads on tray. Food is flatbread rather than baguette; rejected for this bánh-mì story to avoid visual mismatch.',[],[]),
6681020:('Actual frames show a round pie/cake in a dish being put into oven, despite source description saying bread. Rejected: wrong food for this story.',[],[]),
30319062:('Actual frames show mixed meat/herbs in an open foam box on a food stall, baguettes only in background. Correct as takeaway-food ingredients context, not hero bread assembly.',['ingredients','shop','market'],[.1,3.95]),
30790585:('Vendor chops roast pork at street cart with motorbikes arriving/passing. Vietnamese street-food setting per source; no fictional-person identity. Supports shop work/ingredients context.',['ingredients','shop','market'],[.1,7.05]),
3943588:('Close landscape view of anonymous hands unwrapping paper bag and tearing baguette against plain grey background. Final bread split visible. Strong bread texture/quantity generic visual.',['bread'],[.15,14.35]),
3943592:('Portrait view hands unwrap and tear baguette against grey background, same production set as3943588. Crop hands+bread carefully; avoid near-adjacent repeats of same action.',['bread'],[.15,11.35]),
8233041:('Portrait real flour sifting: hand shakes sieve above flour pile; powder falls and pile develops. 66sec source contains ongoing action, but do not spend all duration on repeated sifting or treat flour pile as finished bread.',['flour','ingredients','bakery'],[.2,66.35]),
11196382:('Landscape close-up: coarse flour/bran shaken through metal sieve into metal bowl, accumulating sifted flour visible. Supports ingredient process, not specific flour price or imported origin.',['flour','ingredients'],[.15,13.15]),
3325985:('Hands shake flour sieve above a bowl in sunlit kitchen; powder falls visibly and arm moves. Supports baking ingredients/process only.',['flour','ingredients','bakery'],[.15,13.65]),
}
for a in d['assets']:
    vid=int(a['pexelsID'])
    if vid not in notes:continue
    observation,tags,interval=notes[vid]
    a['tags']=tags
    a['inspection'].update(status='inspected' if interval else 'rejected',method='seven_source_frames_contact_sheet_opened',observations=observation,continuousAVReview=False,frameSamplesOpened=7,fictionalIdentityNotEstablished=True)
    a['usableIntervals']=[{'start':interval[0],'end':interval[1],'role':'illustrative footage; no fictional identity or numeric proof'}] if interval else []
    a['usableForBreadFilm']=bool(interval)
    a['licenseEvidence']={'assetPage':a['pageURL'],'licensePage':'https://www.pexels.com/license/','checkedDateLocal':'2026-11-15','basis':'Primary Pexels asset pages/search results describe Free/Free to use and link Pexels License; official license permits downloading/modification/social-media use, restricts implied endorsement and unaltered resale.','pageAccessLimit':'Direct HTML requests can return Cloudflare403; actual primary content retrieved through web tool; direct media GET succeeded.'}
    rec=ROOT/'research/asset-receipts'/f"{a['id']}.json"
    rec.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
d['summary']={'downloadedSources':len(d['assets']),'downloadedSeconds':round(sum(a['durationSeconds'] for a in d['assets']),2),'inspectedSources':sum(a['inspection']['status']=='inspected' for a in d['assets']),'rejectedSources':sum(a['inspection']['status']=='rejected' for a in d['assets']),'usableSecondsBeforeEdit':round(sum(sum(q['end']-q['start'] for q in a['usableIntervals']) for a in d['assets']),2),'reviewScope':'Opened actual 7-frame source contact sheet for each24source. Not continuous audiovisual review. Shot-level final crop and pacing review still required.'}
d['failed']=[x for x in d.get('failed',[]) if x['id'] not in {a['id'] for a in d['assets']}]
path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(d['summary'],ensure_ascii=False))
