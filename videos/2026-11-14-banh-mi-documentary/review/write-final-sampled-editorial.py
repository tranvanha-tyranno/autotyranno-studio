import hashlib,json
from pathlib import Path

BATCH=Path(__file__).resolve().parent.parent
ROOT=BATCH.parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
final=BATCH/'r02/final.mp4'
plan=BATCH/'r02/props.json'
sheet_numbers=[2,3,5,8,9,10,11,12,13,14,15]
sheets=[BATCH/'r02/qa'/f'contact-{i:02}.jpg' for i in sheet_numbers]
data={
  'schema':'bread-documentary-final-sampled-editorial/1',
  'revision':'r02','dateLocal':'2026-11-15 Asia/Saigon',
  'reviewer':{'kind':'agent','name':'long_content_a independent source and sampled-frame reviewer'},
  'render':{'path':final.relative_to(ROOT).as_posix(),'sha256':sha(final)},
  'plan':{'path':plan.relative_to(ROOT).as_posix(),'sha256':sha(plan)},
  'method':'actual_final_render_contact_sheets_opened_against_script_and_plan',
  'scope':{
    'openedSheetCount':len(sheets),
    'coverageDescription':'Actual final-render sheet02,03,05 for cost and price math;08–15 for b13-03 through final b24-03. Three selected final-frame samples per shot. This is sampled image inspection, not a complete moving-film or listening review.',
    'continuousAVReview':False,'audioListened':False,'allFramesViewed':False,
    'contactOrderCaution':'Sheet columns are alphabetically early,late,middle; read the labels. They are not a playback sequence and cannot establish exact transition feel.',
    'userApproval':'pending_not_established',
    'sheets':[{'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)} for p in sheets]
  },
  'observations':[
    {'shotIds':['b03-02','b04-01'],'start':28.8,'end':54.23,'evidence':['contact-02.jpg'],'observation':'Selected math states show20.000đ selling price with12.000đ input and5.000đ fixed-per-loaf allocation, caveat not net profit. Following actual final frames show the short statement3.000đ chưa phải lãi ròng. Numbers are inside frame, no obvious cutoff. The baguet­te-breaking background is actual bread but does not establish any price.','decision':'selected_cost_states_readable'},
    {'shotIds':['b05-02','b06-02'],'start':54.23,'end':79.2,'evidence':['contact-03.jpg'],'observation':'b05 selected old-price state20.000đ has14.500đ input +5.000đ fixed and500đ remaining; late state22.000đ shows2.500đ remaining and−500đ change. b06 shows3.000→2.500 with customer+2.000 and input+2.500. This matches the illustrative model and distinguishes selling-price increase from retained amount. Real flour/oven visuals remain context.','decision':'selected_new_cost_and_margin_states_match_script'},
    {'shotIds':['b08-02'],'start':98.9,'end':112.63,'evidence':['contact-05.jpg'],'observation':'Actual final middle/late states show20.000→22.000→22.440 with+10% then+2%, and phraseTăng chậm hơn. Giá vẫn cao hơn. The numerical level rises even as the growth rate falls. Illustration and same-quantity caveats visible; units not clipped.','decision':'selected_price_path_matches_script'},
    {'shotIds':['b13-03','b14-01','b14-02','b14-03','b14-04'],'start':179.83,'end':199.5,'evidence':['contact-08.jpg'],'observation':'Receipt terminal, produce-market card transaction and grocery bagging appear at the discussion of costs, possible surplus and customer choices. These are recognizable actions, not blank cards. People/location are generic stock and must not be called Hạnh or her real customers. Foreign market context does not demonstrate the fictional bakery total cost.','decision':'contextual_stock_only'},
    {'shotIds':['b15-01','b15-02','b15-03','b15-04','b16-01'],'start':199.5,'end':220.3,'evidence':['contact-09.jpg'],'observation':'Receipt checking, dough handling, flour shaping and actual Vietnamese baguette filling lead into a calculator/documents shot and buyer-side question. Hands and principal objects visible; no black portrait bars observed in this sample set. Distant receipt writing is not the script’s illustrative financial statement.','decision':'sampled_crops_keep_main_actions'},
    {'shotIds':['b17-01','b17-02','b17-03'],'start':230.37,'end':244.3,'evidence':['contact-10.jpg'],'observation':'Chapter4 heading asks about wage versus bread buying; backgrounds are flour shaping and dough lifting. They anchor bread production but do not show wage, payslip or household earnings, so narration carries the wage premise until the next graphic.','decision':'semantic_limit_not_claimed_as_direct_evidence'},
    {'shotIds':['b18-02'],'start':245.8,'end':256.8,'evidence':['contact-11.jpg'],'observation':'Selected final graphic states show500→477 ổ and approximately−4,5% with caveat that nobody buys only bread and one item does not represent household purchasing power/CPI. Actual hands tear bread behind the right-side graphic. Early/middle state contains500 before477 is introduced; not a missing final number.','decision':'selected_purchasing_power_states_match_script'},
    {'shotIds':['b19-01','b19-02','b19-03','b19-04','b20-01','b20-02','b20-03'],'start':261.53,'end':293.57,'evidence':['contact-11.jpg','contact-12.jpg'],'observation':'More-money/fewer-bread conclusion runs over kneading/oven footage; broader household-spending caveat moves to grocery item selection and checkout handling. Bread/hand subjects stay visible after portrait-to-landscape cropping, although some views are very close. No portrait black side pillars in these selected final pixels.','decision':'crop_checks_scoped_to_selected_frames'},
    {'shotIds':['b21-01','b21-02','b21-03','b21-04','b22-01'],'start':293.57,'end':314.87,'evidence':['contact-13.jpg'],'observation':'Different shopper baskets and transactions support the point that household spending experiences differ. Chapter5 and price/cost/purchasing-power synthesis appear over real dough action; source shoppers remain illustrative, not data proving a local inflation claim.','decision':'contextual_stock_with_clear_explanatory_narration'},
    {'shotIds':['b22-02','b22-03','b23-01','b23-02','b23-03','b23-04'],'start':314.87,'end':342.9,'evidence':['contact-14.jpg','contact-15.jpg'],'observation':'Concluding questions use repeated dough kneading and baguette oven sets. Main hands/dough remain visible, no slide cards or cartoon cast in these selected frames. Visual variety is limited despite nonoverlapping source intervals.','decision':'repetition_limit_recorded'},
    {'shotIds':['b24-01','b24-02','b24-03'],'start':342.9,'end':357.77,'evidence':['contact-15.jpg'],'observation':'CTA asks about breakfast price; moves from hand kneading and gloved shaping into actual Vietnamese baguette sandwich filling/wrapping. Late sample has hand leaving prep board after wrapping, not a frozen empty ending. No full-time subtitles or cartoon visible; short question label appears on first CTA shot.','decision':'bread_callback_present_in_selected_final_closing'}
  ],
  'issues':[
    {'severity':'editorial_limit','shotIds':['b16-02','b16-03','b17-01','b17-02','b17-03','b19-01','b19-02','b19-03','b19-04','b22-02','b22-03','b23-01','b23-02','b23-03','b23-04','b24-01','b24-02'],'observation':'Several consecutive/recurrent units alternate only a few recognizable kneading/oven sets. Different nonoverlapping intervals do not by themselves yield creative or semantic variety.','action':'Retain this limitation for user feedback and future shot selection; do not label the style professional/approved from frame count or source diversity.'},
    {'severity':'semantic_limit','shotIds':['b17-01','b17-02','b17-03'],'observation':'Wage-increase passage is contextual bread making rather than visible wage/payslip comparison. The mathematical purchasing-power explanation only becomes visible inb18.','action':'Do not claim every clause has direct visible evidence; future correction can add actual contextual payroll/personal-budget action if it improves this passage.'},
    {'severity':'scope_limit','observation':'No actual continuous listening or playback performed for this final-film inspection; short fades, spoken emphasis, music feel and perceived pace remain unverified by this report.','action':'Keep final aesthetic/user approval pending.'}
  ],
  'summaryDecision':'selected_final_frame_readability_checked_with_editorial_limits_no_whole_film_acceptance',
  'technicalQA':'Recorded separately inr02/qa-report.json; this report does not replace full decode or audio measurement.'
}
(BATCH/'review/final-sampled-editorial.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Saved final-sampled-editorial.json; render SHA256',data['render']['sha256'])
