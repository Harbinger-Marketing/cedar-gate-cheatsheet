# -*- coding: utf-8 -*-
import html, hashlib, sys, json
IMG_MODE = ('--photos' in sys.argv)   # standalone version embeds real <img> headshots (renders outside the sandbox)

REPCOLOR = {
 "Troy Williams":"#1f3a5f","Stephen Mitchell":"#2f6b3d","Elijah Lee":"#5a3e85",
 "Graham Turner":"#1f6b6b","Lane McPherson":"#9c5a1f","David Harbin":"#7a4a2b","Current Partner":"#1a7f4b",
 "Michael Pollard":"#41617f","Mitchell Attaway":"#6b7785","Justin Culbertson":"#8a6d3b","Parrish Walton":"#5e7d8a",
}

def initials(name):
    parts=[p for p in name.replace("/"," ").split() if p[:1].isalpha()]
    if not parts: return "?"
    if len(parts)==1: return parts[0][:2].upper()
    return (parts[0][0]+parts[-1][0]).upper()

def avatar(p):
    col=REPCOLOR.get(p["rep"],"#444")
    ini=initials(p["name"])
    if IMG_MODE and p.get("photo"):
        return ('<span class="avwrap"><img class="avimg" src="'+html.escape(p["photo"])+
                '" onerror="imgFail(this)" title="'+html.escape(p["name"])+
                '"><div class="av" style="background:'+col+';display:none">'+ini+'</div></span>')
    inner=f'<div class="av" style="background:{col}">{ini}</div>'
    if p.get("photo"):
        return f'<a href="{html.escape(p["photo"])}" target="_blank" title="Open photo" class="avlink">{inner}<span class="cam">photo</span></a>'
    return inner

def chips(p):
    out=[]
    out.append(f'<span class="chip rep" style="background:{REPCOLOR.get(p["rep"],"#444")}">{html.escape(p["rep"])}</span>')
    if p.get("role"): out.append(f'<span class="chip role">{html.escape(p["role"])}</span>')
    if p.get("badge")=="UNCONFIRMED": out.append('<span class="chip unc">UNCONFIRMED</span>')
    if p.get("overnight"): out.append('<span class="chip ov">OVERNIGHT</span>')
    if p.get("client"): out.append('<span class="chip cl">CLIENT</span>')
    return "".join(out)

def links(p):
    L=[]
    if p.get("linkedin"): L.append(f'<a href="{html.escape(p["linkedin"])}" target="_blank">LinkedIn</a>')
    if p.get("website"): L.append(f'<a href="{html.escape(p["website"])}" target="_blank">Website</a>')
    if p.get("photo"): L.append(f'<a href="{html.escape(p["photo"])}" target="_blank">Photo</a>')
    return " &middot; ".join(L) if L else '<span class="muted">no links</span>'

def contact(p):
    bits=[]
    if p.get("email"): bits.append(html.escape(p["email"]))
    if p.get("phone"): bits.append(html.escape(p["phone"]))
    if p.get("team"): bits.insert(0,f'<b>Team {html.escape(p["team"])}</b>')
    return " &middot; ".join(bits)

def card(p):
    note=f'<div class="note">{html.escape(p["note"])}</div>' if p.get("note") else ""
    return f'''<div class="card">
      <div class="cardtop">{avatar(p)}<div class="who"><div class="nm">{html.escape(p["name"])}</div>
      <div class="co">{html.escape(p["company"])}</div></div></div>
      <div class="chips">{chips(p)}</div>
      {stars_html(p.get("fit"))}
      <div class="meta">{contact(p)}</div>
      <div class="links">{links(p)}</div>
      {note}
    </div>'''

# ---------------- DATA ----------------
# rep = assigned Harbinger person; role = SHOOTER/OWNER/etc.
P = {}
def add(key,**kw): P[key]=kw

# OVERNIGHT principals (also at shoot)
add("munday", name="Scott Munday", company="B&H Construction / GES", rep="Elijah Lee", role="Cabin 1 / Dean Baker (Midtown Constr.)",
    team="4", email="scott@bhboring.com", phone="(405) 409-4158", website="https://www.ges.energy",
    photo="https://cdn.prod.website-files.com/67c0f77adae0f033d887d486/683f43a5380f2d209b647631_GES_250501-19.jpg",
    overnight=True, badge="CONFIRMED", note="Referral hub - named across many deals. Photo is from GES site (verify it's him).")
add("walls", name="Kevin Walls", company="Echo Contracting", rep="Elijah Lee", role="Cabin 2 / Eddy",
    team="4", email="kevin@echo-contracting.com", phone="(405) 401-7162", website="https://www.echo-contracting.com",
    linkedin="https://www.linkedin.com/in/kevin-walls-22074b71/", overnight=True, badge="CONFIRMED",
    note="Proposal presented; verbally confirmed - warmest open deal.")
add("eddy", name="Eddy (last name TBD)", company="Echo Contracting", rep="Elijah Lee", role="Cabin 2 (w/ Kevin Walls)",
    website="https://www.echo-contracting.com", overnight=True, badge="CONFIRMED",
    note="Second Echo Contracting attendee, here with Kevin Walls (overnight + Friday). Last name TBD. Echo's shoot team also includes Jordan Hayes & Steve Holloway.")
add("chaney", name="David Chaney", company="Legacy & Succession", rep="David Harbin", role="Cabin 4 / Chris Miller",
    team="5", email="David@legacysuccession.com", phone="(405) 614-2007", website="https://legacysuccession.com",
    linkedin="https://www.linkedin.com/in/davidchaneychfc/",
    photo="https://cdn.prod.website-files.com/691111b36cbdfb41187af5f6/6983c14abeb37afb3364e4de_hf_20260129_194733_c40fe143-aaef-4e41-9361-0c308d74ebc3-Photoroom.png",
    overnight=True, client=True, badge="CONFIRMED", note="Harbinger client; powerful connector to OK business owners.")
add("gorton", name="John Gorton", company="First National Bank & Trust (FNBT)", rep="Stephen Mitchell",
    team="1", email="JGorton@bankfnbt.com", website="https://www.bankfnbt.com",
    linkedin="https://www.linkedin.com/in/john-gorton-0208b084/", overnight=True, client=True, badge="CONFIRMED",
    role="Cabin 3", note="Harbinger client (WON ~$372K). CEO of 130-yr community bank. Bringing Ed Stanton (overnight, Cabin 3) + Brad Wilkerson & Jerry Bethea (Friday shoot).")
add("hoey", name="Philip Hoey (+ Wayne Richards)", company="Hoey Construction", rep="David Harbin",
    team="2", email="philh@hoeyconstruction.com", website="https://hoeyconstruction.com",
    linkedin="https://www.linkedin.com/in/philip-hoey-27867629/",
    photo="https://cdn.prod.website-files.com/69a0112dd5d06fd93d39669c/69fdd509dc1e72c50e4c34ec_philip-hoey.webp",
    overnight=True, client=True, role="Cabin 5", badge="CONFIRMED", note="Harbinger client; bringing the bourbon Thursday night. Cabin 5 w/ Wayne Richards (War Metals).")
add("bowden", name="Kye Bowden (+ wife)", company="KB Electric", rep="David Harbin", role="Cabin 4",
    email="kye@kbelectricllc.net", website="https://kbelectric.online",
    linkedin="https://www.linkedin.com/in/kye-bowden-506365185/", overnight=True, client=True, badge="CONFIRMED",
    note="Existing client (Ellie Lee manages day-to-day). Overnight relationship guest.")
add("fox", name="Mike Fox", company="RPX Technologies", rep="David Harbin", role="cabin w/ Chaney",
    website="https://www.rpxtech.com", linkedin="https://www.linkedin.com/in/ideas2revenue/",
    photo="https://d2gjqh9j26unp0.cloudfront.net/profilepic/995a410dca66eac1ab1339bc49e7773c",
    overnight=True, badge="CONFIRMED", note="David Chaney's cabin partner; Stillwater OK tech firm.")
add("miller", name="Chris Miller", company="One Atlanta Tax Solutions", rep="David Harbin", role="Cabin 4 / overnight",
    overnight=True, badge="CONFIRMED", note="Legacy overnight group (David's guest); Atlanta tax solutions firm.")
add("brock", name="Marc Brockhaus", company="Dunlap Codding", rep="David Harbin", role="Main Cabin / overnight",
    website="https://www.dunlapcodding.com", overnight=True, badge="CONFIRMED",
    note="Legacy overnight group (David's guest); Dunlap Codding IP law firm, OKC.")
add("dbaker", name="Dean Baker", company="Midtown Construction", rep="Elijah Lee", role="Cabin 1 (w/ Scott Munday)",
    overnight=True, badge="CONFIRMED", note="Came with GES/Scott Munday; construction = core ICP. Confirm exact firm/role.")
add("msmith", name="Wayne Richards", company="War Metals", rep="Troy Williams", role="Cabin 5 (w/ Phil Hoey)",
    overnight=True, badge="CONFIRMED", note="Phil Hoey's guest - replaced Matt Smith (can no longer attend). War Metals.")
add("stanton", name="Ed Stanton", company="Company TBD (FNBT guest)", rep="Stephen Mitchell", role="Cabin 3 (w/ John Gorton)",
    overnight=True, badge="CONFIRMED", note="John Gorton's (FNBT) overnight guest - fills Cabin 3 Room 2. Company not yet identified; ask John/Anna.")
add("wilkerson", name="Brad Wilkerson", company="Guest of FNBT (John Gorton)", rep="Stephen Mitchell",
    badge="CONFIRMED", note="John Gorton's (FNBT) Friday-shoot guest (coordinated via Anna).")
add("bethea", name="Jerry Bethea", company="Guest of FNBT (John Gorton)", rep="Stephen Mitchell",
    badge="CONFIRMED", note="John Gorton's (FNBT) Friday-shoot guest (coordinated via Anna).")

# SHOOT-DAY confirmed (not overnight)
add("brad", name="Brad Wittrock / Tiffany Jones", company="TerraStar Inc.", rep="Graham Turner",
    team="4", email="brad.wittrock@terrastarinc.com", phone="405-200-1336", website="https://www.terrastarinc.com",
    linkedin="https://www.linkedin.com/in/brad-wittrock-51350943/", badge="CONFIRMED", note="Qualified; lunch + invite call this week.")
add("carter", name="David Carter", company="Summit Technology Group", rep="Elijah Lee",
    team="3", email="david.carter@stgok.com", phone="405-210-3068", website="https://www.stgok.com",
    linkedin="https://www.linkedin.com/in/stgok-dcarter/",
    photo="https://pronto-core-cdn.prontomarketing.com/2/wp-content/uploads/sites/1676/cache/2026/06/David-bio-pic/66257758.jpg",
    badge="CONFIRMED", note="Discovery completed 6/17 - hot. Team of 3 (open 4th seat).")
add("kirk", name="Kirk Brown", company="K&C Manufacturing", rep="Elijah Lee", role="Elijah shoots here",
    team="2", email="kirk@kcmfg.us", phone="(580) 362-7496", website="https://kcmfg.us",
    linkedin="https://www.linkedin.com/in/kirk-brown-8b211969/", badge="CONFIRMED",
    note="Elijah's squad. Note: K&C recently merged into Century Industries.")
add("avery", name="Avery Smith", company="ORCA (OK Roofing Contractors Assn.)", rep="Elijah Lee",
    team="4", email="avery@orcagroup.org", phone="(405) 436-0547", website="https://orcagroup.org",
    badge="CONFIRMED", note="Exec Director - high-value connector. LinkedIn findable; verify manually.")
add("pfeil", name="Joshua Pfeil", company="Kodiak Gas Services", rep="Elijah Lee",
    team="4", email="joshua.pfeil@kodiakgas.com", website="https://www.kodiakgas.com",
    badge="CONFIRMED", note="Large public energy co. Primary CRM contact is the CMO.")
add("miranda", name="Derick Miranda", company="Dolese Bros.", rep="Elijah Lee",
    team="4", email="dmiranda@dolese.com", website="https://dolese.com", badge="CONFIRMED",
    note="100+ yr OK concrete institution (3 + 1 child).")
add("redsch", name="Red (Steve) Schulze", company="B&H Construction/GES (Team 2)", rep="Elijah Lee",
    team="4", email="red@bhbroing.com", website="https://www.bhboring.com", badge="CONFIRMED",
    note="Heads B&H marketing & sales - strongest net-new prospect.")
add("priddy", name="Shawn Priddy", company="Cultural Discipline", rep="Elijah Lee",
    team="4", email="shawn@culturaldiscipline.com", website="https://culturaldiscipline.com",
    linkedin="https://www.linkedin.com/in/shawn-priddy-88608171/",
    photo="https://vibe.filesafe.space/1778943883235285755/attachments/2fcb5890-d2a3-41b8-bf11-32138c50d27c.png",
    badge="CONFIRMED", note="Advocate program; has referred to Elijah.")
add("erik", name="Erik Van Winkle", company="AIR Technologies", rep="Graham Turner",
    team="4", email="evanwinkle@airtech-ok.com", website="https://www.airtech-ok.com", badge="CONFIRMED",
    note="Same company/team as TJ Green. (Public 'Erik Van Winkle' LinkedIn is NOT him.)")
add("tj", name="TJ Green", company="AIR Technologies", rep="Graham Turner",
    team="4", email="tjgreen@airtech-ok.com", website="https://www.airtech-ok.com", badge="CONFIRMED",
    note="Coordinate with Erik - same foursome.")
add("alvin", name="Alvin Myers (+ Kevin King)", company="United Systems", rep="Graham Turner", role="Graham shoots here",
    team="2", email="amyers@unitedsystemsok.com", phone="405-826-2302", website="https://unitedsystemsok.com",
    linkedin="https://www.linkedin.com/in/alvin-myers-43b521/",
    photo="https://www.datocms-assets.com/147131/1751992727-alvin-myers.jpeg",
    badge="CONFIRMED", note="Just confirmed on the Evite (2 guests).")
add("kking", name="Kevin King", company="United Systems", rep="Stephen Mitchell",
    team="2", email="kking@unitedsystemsok.com", phone="(405) 365-6458", website="https://unitedsystemsok.com",
    badge="CONFIRMED", note="United Systems lead now that Alvin Myers had to drop (funeral + wife's knee surgery). Kevin is at registration; bringing Josh Parrish.")
add("joshp", name="Josh Parrish", company="United Systems", rep="Stephen Mitchell",
    team="2", email="kking@unitedsystemsok.com", badge="CONFIRMED",
    note="New United Systems attendee, here with Kevin King. Registration email being sent (use Kevin's email until Josh's is captured).")
add("doug", name="Doug Benson", company="Beene Services", rep="Lane McPherson", role="Lane shoots here",
    team="2", email="dbenson@beene.cc", phone="918-451-9081", website="https://beene.cc",
    linkedin="https://www.linkedin.com/in/doug-benson-18a3b43a/", badge="CONFIRMED", note="Lane's connection; Troy meeting Wed.")
add("denny", name="Denny Hight", company="The Phoenix Group", rep="Troy Williams", role="OWNER (not shooting)",
    team="4", email="dennyhight@phoenix-grp.com", website="https://phoenixgroupenvironmental.com",
    linkedin="https://www.linkedin.com/in/denny-hight-4174a382/", client=True, badge="CONFIRMED",
    note="Client (WON ~$212K); won the day at a prior Cedar Gate shoot.")
add("garrett", name="Garrett Hight", company="The Phoenix Group (Team 2)", rep="Troy Williams", role="OWNER (not shooting)",
    team="4", email="garretthight@phoenix-grp.com", website="https://phoenixgroupenvironmental.com",
    client=True, badge="CONFIRMED", note="Same firm as Denny.")
add("horgan", name="Joe Horgan", company="MidCentral Energy", rep="Stephen Mitchell",
    team="4", email="jhorgan@midcentralenergy.com", website="https://midcentralenergy.com",
    linkedin="https://www.linkedin.com/in/joe-horgan-577412116/",
    photo="https://midcentralenergy.com/wp-content/uploads/2023/07/joe.jpg",
    badge="CONFIRMED", note="VP Ops; former MLB pitcher - great icebreaker.")
add("urbanc", name="Roy Urbanc (+ Koby Penny)", company="JPMorgan (verify - may be First Citizens now)", rep="Stephen Mitchell",
    team="2", email="roy.p.urbanc@jpmorgan.com", linkedin="https://www.linkedin.com/in/roy-urbanc-287231299",
    badge="CONFIRMED", note="Commercial banker - two-way referral partner.")
add("boyd", name="Robert Boyd", company="Jimmie L. Dean Scholarship Foundation", rep="Stephen Mitchell",
    team="4", email="info@jimmiedeanfoundation.org", website="https://www.jimmiedeanfoundation.org",
    badge="CONFIRMED", note="Community connector (nonprofit).")
add("strider", name="Allen Strider", company="KLX Energy Services (verify)", rep="Troy Williams", role="OWNER (not shooting)",
    team="4", email="rstrider2@outlook.com", website="https://klx.com",
    linkedin="https://www.linkedin.com/in/r-allen-strider-8422a0120/", badge="CONFIRMED",
    note="On Toby Keith & CASA clay-shoot committees.")
add("robber", name="Mike Robberson", company="Twisted Oak LLC", rep="Troy Williams", role="OWNER (not shooting)",
    team="4", email="mike.robberson@yahoo.com", website="https://twistedoakllc.com",
    linkedin="https://www.linkedin.com/in/mike-robberson-036354185", badge="CONFIRMED",
    note="Real estate; bringing Stedman, Lemming, Johnson.")
add("bradford", name="Jeremy Bradford", company="Bending Steel (verify)", rep="Troy Williams", role="OWNER (not shooting)",
    team="4", email="bradfordc_44@yahoo.com", website="https://bendingsteel.farm", badge="CONFIRMED",
    note="RSVP'd 'Looking forward to it!' Company unverified.")
add("ward", name="Gary Ward", company="Company TBD", rep="Troy Williams", role="OWNER (not shooting)",
    team="4", email="gward11deer@yahoo.com", badge="CONFIRMED", note="Company not identified - get from inviter.")
add("zamora", name="Anthony Zamora", company="Company TBD", rep="Michael + Mitchell",
    team="2", email="zamora_anthony1200@yahoo.com", badge="CONFIRMED", note="Company not identified; Michael & Mitchell fill the squad.")
add("colt", name="Colt Hunter", company="Southern Lifting & Hoisting", rep="David Harbin", role="on Hoey squad",
    team="1", email="colt.hunter@southernliftingandhoisting.com", website="https://www.southernliftingandhoisting.com",
    badge="CONFIRMED", note="Heavy-haul/crane; unknown inviter - greeting owned by Troy.")
add("ortiz", name="David Ortiz", company="Legacy & Succession (Team 2)", rep="David Harbin",
    team="4", email="ortiz@legacysuccession.com", website="https://legacysuccession.com",
    linkedin="https://www.linkedin.com/in/david-ortiz-exit-planner/",
    photo="https://cdn.prod.website-files.com/691111b36cbdfb41187af5f6/6983c12818a1a63e92893ac6_hf_20260129_190025_abb52303-fa7f-4eae-a52d-cc92761dc98b-Photoroom.png",
    client=True, badge="CONFIRMED", note="Harbinger client firm; exit planner.")

# UNCONFIRMED (chasing) - shoot page only
add("toms", name="Matthew Toms", company="Bostick Services", rep="Lane McPherson",
    team="4", email="mltoms1212@gmail.com", phone="(405) 657-9296", website="https://bostickservicescorp.com",
    linkedin="https://www.linkedin.com/in/matthew-toms-840026175", badge="UNCONFIRMED")
add("hayden", name="Hayden McCalman", company="Harbor Insurance", rep="Justin Culbertson",
    team="3", email="hmccalman@harborinsok.com", phone="(918) 809-4465", website="https://www.harborinsok.com",
    linkedin="https://www.linkedin.com/in/hayden-mccalman-24137220a/",
    photo="https://cdn.theorg.com/bba4f8be-0108-4d23-93a7-879ae331117f_thumb.jpg", badge="UNCONFIRMED")
add("morrow", name="Daniel Morrow", company="Coreslab Structures", rep="Parrish Walton",
    team="3", email="dmorrow@coreslab.com", phone="(405) 885-5442", website="https://www.coreslab.com", badge="UNCONFIRMED")
add("sean", name="Sean Cooper", company="Sean U. Cooper Construction", rep="Lane McPherson",
    team="3", email="sean@seanucooper.com", phone="(918) 704-0126", website="https://www.seanucooper.com",
    linkedin="https://www.linkedin.com/in/sean-cooper-07128353/", badge="UNCONFIRMED")
add("kates", name="Chris Kates", company="Midwest Wrecking Co.", rep="Lane McPherson",
    team="3", email="chris@midwestwreckingco.com", phone="(405) 550-7206", website="https://www.midwestwreckingco.com",
    linkedin="https://www.linkedin.com/in/chris-kates-51a6a48b/", badge="UNCONFIRMED", note="Chris not attending personally - team comes.")
add("cook", name="Collin Cook", company="Reroof America", rep="Lane McPherson",
    team="4", email="ccook@reroofamerica.com", phone="405-755-3000", website="https://www.reroofamerica.com",
    linkedin="https://www.linkedin.com/in/collingcook/", badge="UNCONFIRMED")
add("buster", name="Buster Bradshaw", company="Paladin Land Group", rep="Lane McPherson",
    team="4", email="jbradshaw@paladinlandgroup.com", phone="(405) 880-3594", website="https://paladin.land",
    linkedin="https://www.linkedin.com/in/jeremiah-m-%E2%80%9Cbuster%E2%80%9D-bradshaw-0664781b/", badge="UNCONFIRMED")
add("page", name="Layne Page", company="The Beckman Company", rep="Lane McPherson",
    team="3", email="lpage@beckmancompany.com", phone="405-842-2337", website="https://www.beckmancompany.com",
    linkedin="https://www.linkedin.com/in/layne-page-214273252", badge="UNCONFIRMED")
add("jessup", name="Jason Jessup", company="Timberwolf Excavating", rep="Lane McPherson",
    team="3", badge="UNCONFIRMED", note="Newly added by Lane - contact pending.")
add("amilian", name="Matt Amilian", company="Mach Energy Services", rep="Graham Turner",
    email="mamilian@machenergyllc.com", phone="405-439-4000", website="https://machenergyllc.com",
    linkedin="https://www.linkedin.com/in/matt-amilian-b42a6239", badge="UNCONFIRMED")
add("tara", name="Tara Bashaw", company="Allied Towing of Tulsa", rep="Graham Turner",
    email="tara@towtulsa.com", phone="918-438-0288", website="https://www.towtulsa.com", badge="UNCONFIRMED",
    note="Now President of Storey Wrecker (affiliated).")
add("tamara", name="Tamara Johnson", company="Gateway Co.", rep="Graham Turner",
    email="hr@gatewayok.com", phone="405-285-5884", website="https://gatewayok.com",
    linkedin="https://www.linkedin.com/in/tamara-johnson-9263625a", badge="UNCONFIRMED", note="EA; McGuire family are the principals.")
add("barnes", name="Michael Barnes", company="MacHill Construction", rep="Graham Turner",
    email="michaelbarnes@machillconstruction.com", phone="580-332-1404", website="https://machillconstruction.com",
    linkedin="https://www.linkedin.com/in/michael-barnes-35bb45a", badge="UNCONFIRMED", note="Conflicting event noted.")
add("oquinn", name="Alex O'Quinn", company="Pavement Pro", rep="Graham Turner",
    email="alex@pavementproseal.com", phone="405-544-7129", website="https://pavementproseal.com", badge="UNCONFIRMED")
add("moore", name="Mike Moore", company="Mike's Towing", rep="Graham Turner",
    email="mikestowingllc@hotmail.com", phone="918-519-3820", badge="UNCONFIRMED")
add("lisa", name="Lisa (last name TBD)", company="Preferred Business Systems", rep="Graham Turner",
    email="supply@techbypbs.com", phone="918-252-2199", website="https://techbypbs.com",
    badge="UNCONFIRMED", note="Tulsa office tech / managed IT; owner Mike Wolfinbarger.")
add("hazen", name="Julie Hazen", company="A&A Trucking", rep="Troy Williams",
    email="jhazen@aa-trucking.com", phone="(405) 323-2985", website="https://www.aa-trucking.com",
    badge="UNCONFIRMED", note="Lane's prospect (~2 guests). Marked attending in the tracker but Evite RSVP not yet confirmed; not yet slotted to a team.")

OVERNIGHT_KEYS=["munday","walls","eddy","gorton","stanton","hoey","chaney","miller","brock","dbaker","msmith"]

CONFIRMED_KEYS=["munday","redsch","walls","eddy","kirk","carter","avery","pfeil","miranda","priddy","erik","tj","kking","joshp",
 "brad","doug","gorton","horgan","urbanc","boyd","chaney","ortiz","hoey","colt","miller","brock",
 "denny","garrett","strider","robber","bradford","ward","zamora","dbaker","msmith",
 "stanton","wilkerson","bethea"]
UNCONF_KEYS=["morrow","buster","page"]

REP_ORDER=["Current Partner","Elijah Lee","Stephen Mitchell","Troy Williams","David Harbin","Lane McPherson","Graham Turner"]

# ---- Assignments = previous (post-meeting) list + Michael's update ----
# Base data already reflects the meeting moves (Shawn Priddy->Elijah, Hights->Troy, Munday/Schulze->Elijah).
# Update: no one assigned to Graham or Lane. Graham's people split Elijah/Stephen; Lane's -> Troy.
# Unconnected guests stay with Troy (greeting only), matching the prior list.
REASSIGN={
 # Graham's -> Elijah
 "erik":"Elijah Lee","tj":"Elijah Lee","moore":"Elijah Lee",
 # Graham's -> Stephen
 "brad":"Elijah Lee","alvin":"Stephen Mitchell","amilian":"Stephen Mitchell","tara":"Stephen Mitchell",
 "tamara":"Stephen Mitchell","barnes":"Stephen Mitchell","oquinn":"Stephen Mitchell","lisa":"Stephen Mitchell",
 # Lane's -> Troy
 "doug":"Troy Williams","toms":"Troy Williams","hayden":"Troy Williams","morrow":"Troy Williams",
 "sean":"Troy Williams","kates":"Troy Williams","cook":"Troy Williams","buster":"Troy Williams",
 "page":"Troy Williams","jessup":"Troy Williams",
 # Unconnected guests stay with Troy (as in the prior list)
 "strider":"Troy Williams","zamora":"Troy Williams","ward":"Troy Williams","bradford":"Troy Williams",
 "robber":"Troy Williams","colt":"Troy Williams",
 # David Harbin's overnight group -> Troy for both days (per Michael)
 "chaney":"Troy Williams","hoey":"Troy Williams","miller":"Troy Williams","brock":"Troy Williams",
}
for _k,_r in REASSIGN.items():
    P[_k]["rep"]=_r
for _k in ["doug","alvin","hayden","morrow","colt"]:
    P[_k].pop("role",None)
for _k in P:
    if P[_k]["rep"]=="Troy Williams" and not P[_k].get("role"):
        P[_k]["role"]="OWNER (not shooting)"

# ---- Current partners (existing clients): no prospecting rep; label "Current Partner" ----
CURRENT_PARTNERS={"munday","denny","garrett","gorton","chaney","ortiz","hoey"}
for _k in CURRENT_PARTNERS:
    if _k in P:
        P[_k]["rep"]="Current Partner"
        if P[_k].get("role")=="OWNER (not shooting)":
            P[_k].pop("role",None)

# ---- Unconfirmed stay with their ORIGINAL inviter (Lane or Graham) until they RSVP yes ----
# Only after confirming do they move to their host (Troy / Elijah / Stephen).
UNCONF_INVITER={
 "toms":"Lane McPherson","hayden":"Lane McPherson","morrow":"Lane McPherson","sean":"Lane McPherson",
 "kates":"Lane McPherson","cook":"Lane McPherson","buster":"Lane McPherson","page":"Lane McPherson",
 "jessup":"Lane McPherson","hazen":"Lane McPherson",
 "amilian":"Graham Turner","tara":"Graham Turner","tamara":"Graham Turner","barnes":"Graham Turner",
 "oquinn":"Graham Turner","moore":"Graham Turner","lisa":"Graham Turner",
}
for _k,_r in UNCONF_INVITER.items():
    if _k in P:
        P[_k]["rep"]=_r
        P[_k].pop("role",None)

# ---- Best-fit rating (1-5) vs Harbinger ICP (OK trades/construction/home-services/mfg/energy-svcs) ----
# Grounded in Harbinger's 271-client base: core trades + construction score highest; existing clients = 5;
# enterprises / banks-as-buyers / nonprofits / associations / unknown = low.
FITSCORE={
 "munday":5,"redsch":5,"walls":5,"kirk":4,"carter":4,"avery":3,"pfeil":2,"miranda":2,"priddy":3,
 "erik":4,"tj":4,"brad":4,"alvin":4,"doug":4,"denny":5,"garrett":5,"gorton":5,"horgan":4,"urbanc":2,
 "boyd":2,"strider":2,"zamora":2,"ward":2,"bradford":3,"robber":3,"colt":4,"miller":3,"brock":3,
 "chaney":5,"ortiz":5,"hoey":5,"dbaker":4,"msmith":4,"stanton":3,"wilkerson":3,"bethea":3,"eddy":4,"kking":4,"joshp":3,
 "toms":4,"hayden":4,"morrow":4,"sean":5,"kates":4,"cook":5,"buster":4,"page":4,"jessup":4,
 "amilian":4,"tara":4,"tamara":3,"lisa":4,"barnes":5,"oquinn":4,"moore":2,"hazen":3,
}
for _k,_s in FITSCORE.items():
    if _k in P: P[_k]["fit"]=_s

# ---- Enrichment pass (Asana sweep + web research, Jun 22): headshots, corrected companies, emails, phones ----
ENRICH={
 "brock":{"photo":"https://dunlapcodding.com/wp-content/uploads/2019/02/Marc-Brockhaus-164_Web.jpg",
          "email":"mbrockhaus@dunlapcodding.com","phone":"405-607-8610","website":"https://www.dunlapcodding.com",
          "note":"Legacy overnight group (David's guest); attorney-director, Dunlap Codding (IP law, OKC)."},
 "miller":{"website":"https://www.oneatlantataxsolutions.com","linkedin":"https://www.linkedin.com/in/cmiller33367/",
           "email":"consult@oneatlantataxsolutions.com","phone":"(470) 873-9940",
           "note":"Legacy overnight group (David's guest); Founder/CEO, One Atlanta Tax Solutions (Kennesaw GA)."},
 "dbaker":{"website":"https://www.midtownconstructionok.com","linkedin":"https://www.linkedin.com/in/dean-baker-25252523/",
           "note":"Came with GES/Scott Munday. President, Midtown Construction Services (Edmond OK; a branch of A.C. Owen Construction)."},
 "robber":{"photo":"https://twistedoakllc.com/uploads/3/6/4/8/36483916/published/mike.jpg","email":"mike@twistedoakllc.com",
           "note":"Managing Partner, Twisted Oak (real estate). Team also brings Scott Stedman, Scott Lemming, Matt Johnson."},
 "buster":{"photo":"https://paladin.land/cdn/shop/files/16_e9b1820c-9a1e-439a-939a-dc738006a110.png?v=1752605656&width=1080",
           "phone":"(918) 582-5404","note":"Principal/CEO, Paladin Land Group."},
 "amilian":{"photo":"https://machenergyllc.com/wp-content/uploads/2025/03/Matt-Amilian-HS-scaled.jpg","phone":"405-263-7707",
            "note":"Director of Business Development, Mach Energy Services."},
 "tamara":{"photo":"https://cdn.theorg.com/4cd43375-7de1-4ca1-b846-1f129e756d94_thumb.jpg",
           "note":"Exec Assistant, The Gateway Companies / Gateway Pipeline. McGuire family are the principals."},
 "oquinn":{"photo":"https://pavementproseal.com/wp-content/uploads/2024/12/alex-oquinn.jpg",
           "email":"thepavementpro@gmail.com","phone":"(405) 544-4657","note":"Owner/Founder, PavementPro."},
 "strider":{"company":"FireRock Energy Services","website":"https://firerock.services","email":"allen.strider@firerockservices.com",
            "phone":"(405) 465-3354","linkedin":"https://www.linkedin.com/in/r-allen-strider-8422a0120/",
            "note":"CORRECTED: now FireRock Energy Services (OKC directional drilling), not KLX. On Toby Keith & CASA clay-shoot committees."},
 "urbanc":{"company":"First Citizens Bank (moved from JPMorgan)","email":"roy.urbanc@firstcitizens.com",
           "note":"CORRECTED: VP Business Banking at First Citizens since Nov 2023 - the old JPMorgan email is dead. Brings Koby Penny. Two-way referral partner."},
 "bradford":{"company":"Company unverified","website":"",
             "note":"RSVP'd 'Looking forward to it!' Employer unverified ('Bending Steel Farms' is an OK cattle operation, not his firm). Confirm with inviter."},
 "boyd":{"linkedin":"https://www.linkedin.com/in/robertboyd/","phone":"(918) 585-1220",
         "note":"Chairman/President of the foundation; also founder of Boston Street Advisors (Tulsa). Community connector."},
 "colt":{"phone":"(833) 652-5438","note":"Heavy-haul/crane (Southern Lifting & Hoisting); on Phil Hoey's team. Greeting owned by Troy. Person-company link unverified."},
 "avery":{"phone":"(405) 285-5711","note":"Executive Director, ORCA - high-value connector. No public non-LinkedIn headshot."},
 "jessup":{"name":"Jackson Jessop (a/k/a Jason Jessup)","company":"Timber Wolf Excavating","website":"https://twolfx.com",
           "linkedin":"https://www.linkedin.com/in/jackson-jessop-329a55182","email":"jackson@twolfx.com","phone":"(918) 284-1566",
           "note":"Owner/CEO, Timber Wolf Excavating (Broken Arrow). Name shows as 'Jackson Jessop' in tracker, 'Jason Jessup' on the teams sheet - confirm."},
 "ward":{"note":"Company still unknown. Best lead: 'Gary Ward & Son Excavation' (OK excavation) - UNVERIFIED. Confirm with inviter."},
 "zamora":{"note":"Company still unknown; no confident OK match found. Confirm with inviter who brought him. Michael & Mitchell fill the squad."},
 "msmith":{"note":"Phil Hoey's guest, replacing Matt Smith (can no longer attend). Wayne Richards of War Metals - get email/phone from Phil Hoey. On Hoey's team (Phil, Wayne, Colt Hunter, David)."},
 "lisa":{"note":"Tulsa office tech / managed IT (Preferred Business Systems; owner Mike Wolfinbarger). Last name not yet found - confirm."},
 "robberson_dummy":{},
}
for _k,_d in ENRICH.items():
    if _k in P and _d: P[_k].update(_d)

# ---- Evite verification pass (Jun 22): RSVP emails/phones pulled live from the Evite "Yes" list ----
EVITE={
 "gorton":{"phone":"(405) 761-9165"},
 "denny":{"phone":"(405) 202-8752"},
 "garrett":{"phone":"(405) 479-5279"},
 "robber":{"phone":"(405) 205-4279","email":"mike.robberson@yahoo.com","add_note":"Evite RSVP email; work address mike@twistedoakllc.com."},
 "redsch":{"phone":"(405) 650-4319"},
 "horgan":{"phone":"(281) 475-9316"},
 "zamora":{"phone":"(863) 599-1504"},
 "miranda":{"phone":"(405) 519-9827"},
 "tj":{"phone":"(405) 314-5225"},
 "priddy":{"phone":"(405) 234-0733"},
 "hoey":{"phone":"(918) 271-3886"},
 "pfeil":{"phone":"(405) 823-0193","add_note":"Evite confirms his email + party of 4."},
 "ortiz":{"phone":"(405) 205-3109"},
 "bradford":{"phone":"(405) 320-0458"},
 "ward":{"phone":"(405) 205-1604"},
 "erik":{"phone":"(405) 203-9286"},
 "colt":{"phone":"(580) 922-0092","email":"colt.hunter@southernliftingandhoisting.com"},
 "avery":{"phone":"(405) 436-0547"},
 "strider":{"email":"rstrider2@outlook.com","add_note":"Evite RSVP email/phone above; work address allen.strider@firerockservices.com."},
 "brad":{"add_note":"Evite RSVP came via Tiffany Jones: tiffany.jones@terrastarinc.com, (405) 974-1468."},
 "munday":{"add_note":"Evite RSVP phone alt: (405) 288-2412 (party of 4)."},
 "doug":{"add_note":"Evite RSVP phone alt: (918) 991-3200."},
 "urbanc":{"phone":"(623) 882-5093","add_note":"Evite RSVP email roy.p.urbanc@jpmorgan.com (likely dead - use the First Citizens address)."},
 "alvin":{"add_note":"Kevin King also confirmed on the Evite: kking@unitedsystemsok.com, (405) 365-6458."},
}
for _k,_d in EVITE.items():
    if _k in P:
        if _d.get("phone"): P[_k]["phone"]=_d["phone"]
        if _d.get("email"): P[_k]["email"]=_d["email"]
        if _d.get("add_note"): P[_k]["note"]=(P[_k].get("note","")+" "+_d["add_note"]).strip()

def stars_html(n):
    if not n: return ""
    on='&#9733;'*n; off='&#9733;'*(5-n)
    return ('<div class="fit"><span class="stars">'+on+'<span class="off">'+off+
            '</span></span> <span class="muted">best fit '+str(n)+'/5</span></div>')

def group_by_rep(keys):
    g={}
    for k in keys:
        g.setdefault(P[k]["rep"],[]).append(k)
    return g

def render_groups(keys):
    g=group_by_rep(keys)
    out=[]
    for rep in REP_ORDER:
        if rep not in g: continue
        ks=g[rep]
        col=REPCOLOR.get(rep,"#444")
        cards="".join(card(P[k]) for k in ks)
        out.append(f'<div class="repgroup"><h3 style="border-left:6px solid {col}">{html.escape(rep)} <span class="cnt">{len(ks)}</span></h3><div class="grid">{cards}</div></div>')
    return "".join(out)

overnight_html=render_groups(OVERNIGHT_KEYS)
shoot_conf_html=render_groups(CONFIRMED_KEYS)
shoot_unc_html=render_groups(UNCONF_KEYS)

CABINS_HTML='''
<div class="banner">Thursday-night guest cabins (per Troy's Sleeping Arrangements task). <b>KB Electric removed - no longer attending.</b> Harbinger team lodging is a separate hotel booking.</div>
<div class="grid">
 <div class="card"><div class="nm">Cabin 1 - GES</div><div class="meta" style="margin-top:6px">Room 1: <b>Scott Munday</b> (GES)<br>Room 2: <b>Dean Baker</b> (Midtown Construction)</div></div>
 <div class="card"><div class="nm">Cabin 2 - Echo Contracting</div><div class="meta" style="margin-top:6px">Room 1: <b>Kevin Walls</b><br>Room 2: <b>Eddy</b></div></div>
 <div class="card"><div class="nm">Cabin 3 - FNBT</div><div class="meta" style="margin-top:6px">Room 1: <b>John Gorton</b><br>Room 2: <b>Ed Stanton</b> (FNBT guest)</div></div>
 <div class="card"><div class="nm">Cabin 4 - Legacy &amp; Succession</div><div class="meta" style="margin-top:6px">Room 1: <b>David Chaney</b><br>Room 2: <b>Chris Miller</b> (One Atlanta Tax Solutions)</div></div>
 <div class="card"><div class="nm">Cabin 5 - Hoey Construction</div><div class="meta" style="margin-top:6px">Room 1: <b>Phil Hoey</b><br>Room 2: <b>Wayne Richards</b> (War Metals)</div></div>
 <div class="card"><div class="nm">Main Cabin (dinner venue; 3 rooms)</div><div class="meta" style="margin-top:6px">Room 1: <b>Marc Brockhaus</b> (Dunlap Codding)<br>Room 2: open<br>Room 3: open</div></div>
</div>
'''

RUNOFSHOW_HTML='''
<div class="banner"><b>Run of Show &mdash; v5 (source of truth), refreshed Jun 22, 2026.</b> Step-by-step from leaving the Harbinger office through the event and back, plus every link you need on the day. Items marked <i>Open/CONFIRM</i> still need confirming.</div>
<div class="rosblock"><h3>All event links</h3><ul class="roslist">
<li><b>Raffle kiosk</b> (iPad sign-up to win the Benelli): <a target="_blank" href="https://cedar-gate-raffle.vercel.app/">cedar-gate-raffle.vercel.app</a></li>
<li><b>Raffle admin</b> (draw/redraw winner, export CSV): <a target="_blank" href="https://cedar-gate-raffle.vercel.app/admin">/admin</a> &middot; admin password: <code>cedargate2026</code></li>
<li><b>Discovery booking</b> (Calendly &mdash; same link behind the table QR + closing email): <a target="_blank" href="https://calendly.com/d/ct7g-x3g-mb5/the-harbinger-demo-okc">Harbinger Discovery OKC</a></li>
<li><b>Clay Shoot Evite</b>: <a target="_blank" href="https://evite.me/HarbingerClays">evite.me/HarbingerClays</a></li>
<li><b>Outreach / RSVP tracker</b>: <a target="_blank" href="https://docs.google.com/spreadsheets/d/1O363mPR0ZpvjpsfiJ-3G4XI3LCZS_huZrxk_Mn_W5Pg/edit">Tracker sheet</a></li>
<li><b>Attendee / prospect sheet</b>: <a target="_blank" href="https://docs.google.com/spreadsheets/d/16REPxLEVFuvRX4rkadq_8KiAbGX9l11IMSJD5VCWk1A/edit">Attendee sheet</a></li>
<li><b>Waiver</b> (everyone signs): <a target="_blank" href="https://app.waiversign.com/e/612528c3663fa30019930f0d/doc/61252945663fa30019930fde?eventName=Harbinger%202026">WaiverSign</a></li>
<li><b>Event video</b>: in the "Harbinger Cedar Gate Event Video" Asana task (Dropbox)</li>
<li><b>Venue</b>: Stacey Holden &mdash; 405-370-1952 &middot; sholden@thecedargate.com</li>
</ul></div>
<div class="rosblock"><h3>Who's who &amp; travel</h3><ul class="roslist">
<li><b>Flying Thursday Jun 25 on Delta DL2490 (7):</b> Michael Pollard, Lane McPherson, Graham Turner, Stephen Mitchell, Mitchell Attaway, Parrish Walton, Chris Scott (camera).</li>
<li><b>Flying in earlier with their OWN vehicles</b> (not on the Thursday flight, not in the rentals): Troy Williams, Elijah Lee, David Harbin.</li>
<li><b>Justin Culbertson</b> &mdash; NOT on the Thursday team flight (flying out separately for a meeting); confirm his event arrival.</li>
<li><b>Flight:</b> Delta DL2490, conf# GINV8Z &middot; ATL &rarr; OKC &middot; dep 9:18 AM ET / arr 10:29 AM CT. Be at ATL by ~7:15 AM.</li>
<li><b>Rentals:</b> 2 vehicles (size up to full-size SUV/van) for the 8 flyers + luggage + locked firearm cases + camera gear + supply stops.</li>
<li><b>Lodging:</b> Holiday Inn Express (~6 rooms); re-check Loft (5) vs hotel split for the Thursday-night group.</li>
</ul></div>
<div class="rosblock"><h3>Roles at a glance</h3><ul class="roslist">
<li><b>David Harbin</b> &mdash; host presence; 20-min lunch presentation.</li>
<li><b>Elijah Lee</b> &mdash; setup table with Michael (QR codes, booth, shotgun, signage); partner/prospect host; opens lunch with a prayer.</li>
<li><b>Michael Pollard</b> &mdash; logistics lead / event quarterback; setup table; raffle app + kiosk; runs the day; cues the timed discovery email.</li>
<li><b>Mitchell Attaway</b> &mdash; registration + lunch material setup; owns the registration + raffle kiosk station.</li>
<li><b>Stephen Mitchell</b> &mdash; cabin gift placement (with Parrish); raffle winner announcement + hype; thanks guests at the end.</li>
<li><b>Parrish Walton</b> &mdash; cabin gift placement (with Stephen); partner/prospect host; FFL gun transfer.</li>
<li><b>Lane / Graham / Justin</b> &mdash; water-bottle wrapping + cart prep (2 Harbinger hats per cart).</li>
<li><b>Chris Scott</b> &mdash; camera operator; sets up only his own gear. Key moments: clay shoot, David's talk, raffle draw, candid dinner shots.</li>
</ul></div>
<div class="rosblock"><h3>Thursday, June 25 &mdash; travel, setup &amp; overnight</h3><ul class="roslist">
<li>~6:00 AM &mdash; depart Harbinger office (Tyrone), drive to ATL (CONFIRM exact time; earlier if firearm check needed).</li>
<li>9:18 AM ET &mdash; DL2490 departs ATL &rarr; 10:29 AM CT arrives OKC.</li>
<li>On arrival &mdash; pick up 2 rentals; split supply stops: <b>Vehicle 1 = wine</b> (dinner/cabin gifts), <b>Vehicle 2 = water bottles + snacks</b>. OKC &rarr; Kingfisher ~45 min.</li>
<li><b>~2:00 PM</b> &mdash; team arrives Cedar Gate; setup before guests (cabins should be unlocked &mdash; confirm time with Stacey).</li>
<li><b>Setup split:</b> cabin gifts (Stephen + Parrish) &middot; water bottles + carts (Lane + Graham + Justin) &middot; registration + lunch space at The Carriage House (Michael + Mitchell) &middot; booth / QR / shotgun / signage (Michael + Elijah + Stephen) &middot; iPad kiosk test + reset to zero, confirm Wi-Fi (Michael) &middot; camera gear (Chris).</li>
<li>4:30&ndash;5:00 PM &mdash; guest cabin check-in.</li>
<li>6:30 PM &mdash; dinner at the Lodge (Steak &amp; Salmon); each host sits with their prospects.</li>
<li>8:00 PM &mdash; bourbon tasting / cocktail hour (Hoey's bourbon; Troy picks up).</li>
<li><b>Tell every overnight guest Thursday night:</b> cabin check-out is <b>10:00 AM Friday</b> &mdash; have all belongings out of the cabins before heading over to the shoot.</li>
<li><i>Open:</i> Big Gun / six-stand experience &mdash; confirm with Stacey whether it's on for 2026 and the time.</li>
</ul></div>
<div class="rosblock"><h3>Friday, June 26 &mdash; event day</h3><ul class="roslist">
<li>~7:45 AM &mdash; final setup sweep at The Carriage House (iPad on entry form at zero, Wi-Fi confirmed, registration staffed, QR stands on tables, carts staged).</li>
<li><b>8:30 AM &mdash; registration + breakfast</b> (Cedar Gate Wrap). <b>Combined station (Mitchell owns):</b> fill out the raffle entry on the iPad &rarr; write a handwritten name tag (NAME + COMPANY) &rarr; breakfast. This funnels every walk-on teammate through the iPad so we capture their contact info &mdash; frame it as the entry to win the Benelli. Hosts greet and find their guests; Michael floats; Chris captures.</li>
<li>9:45 AM &mdash; safety training (Cedar Gate staff).</li>
<li><b>10:00 AM &mdash; clay shoot</b> (one course reserved, ~70 shooters; hosts shoot alongside their prospects). Right after: Michael/Mitchell export the raffle CSV from /admin to build the discovery list before lunch.</li>
<li><b>12:00 PM &mdash; lunch (The Chop).</b> Elijah Lee opens with a prayer before everyone eats; hosts sit with their guests.</li>
<li><b>Raffle draw</b> (right after lunch) &mdash; Stephen announces/hypes; use the admin DRAW WINNER button (iPad on a screen if possible). Winner does NOT take the gun on-site &mdash; visits the FFL dealer, completes ATF Form 4473, presents photo ID, passes a NICS check. If they fail, use Redraw for a backup. Capture winner info for the FFL handoff.</li>
<li><b>David's presentation</b> (20 min, after the raffle) &mdash; (1) make your business look as credible as it actually is; (2) what it costs to get a new customer and how to scale it; (3) how to get in front of your best future employees. Close: David invites everyone to book a 1-hour discovery call via the table QR.</li>
<li><b>TIMED SEND</b> &mdash; right as David closes, Michael cues Luke, who fires the discovery email (Mailchimp) to all Evite registrants + raffle entrants. Goal: phones buzz in the room.</li>
<li><b>Wrap</b> &mdash; Stephen thanks guests; hosts lock next steps (book the discovery call on the spot); teardown; export the final raffle CSV before leaving.</li>
<li><b>Return</b> &mdash; Thursday-flight group &rarr; OKC airport, return rentals, fly ATL (Fri evening &mdash; CONFIRM time). Troy/Elijah/David handle their own return.</li>
</ul></div>
<div class="rosblock"><h3>Headcounts &amp; food</h3><ul class="roslist">
<li>Thursday dinner at the Lodge: <b>25</b> (Steak &amp; Salmon).</li>
<li>Friday breakfast (Cedar Gate Wrap) + lunch (The Chop): <b>~140</b> (latest venue confirm; v5 draft said 125 &mdash; reconcile with Stacey).</li>
<li>Clay shoot: one course, <b>~70 shooters</b>; ~35 teams registered. <i>Open:</i> 60 vs 100 target course decision (Michael/Stacey).</li>
</ul></div>
<div class="rosblock"><h3>Key dependencies &amp; open items</h3><ul class="roslist">
<li>Handwritten name tags &mdash; Martha (bring/ship blank write-on tags; no pre-printing).</li>
<li>Tyrone &rarr; ATL departure time &mdash; Michael / Martha.</li>
<li>2 rental vehicles + driver / supply-stop assignments (V1 wine, V2 water + snacks).</li>
<li>Chris Scott travel + lodging (same Thursday flight; +1 hotel room).</li>
<li>Troy / Elijah / David earlier travel + own vehicles (NOT on DL2490).</li>
<li>Thursday-night lodging split &mdash; Loft (5) vs hotel.</li>
<li>Big Gun / six-stand &mdash; confirm on for 2026 + time (Stacey).</li>
<li>Confirm Thursday dinner headcount (25) with Stacey.</li>
<li>Pre-event waiver send (Michael).</li>
<li>Discovery email pre-built in Mailchimp, timed to David's close (Luke); Michael cues.</li>
<li>Combined email list (Evite + raffle entries) &mdash; Michael / Mitchell.</li>
<li>QR code stands printed + acrylic holders (design / ops).</li>
<li>Shotgun inventory + locked travel cases + locks (everyone flying needs a gun); confirm firearm travel with Delta.</li>
<li>Confirm what's already shipped (Martha).</li>
</ul></div>
<div class="rosblock"><h3>Packing / shipping</h3><ul class="roslist">
<li>Ship large materials ahead to: <b>209 French Park, Suite 103, Edmond, OK 73034</b> (Stacey's office; she delivers to the property). Confirm what's shipped with Martha.</li>
<li>Carry with the team: iPad (raffle kiosk) + charger + backup battery; Chris's camera gear (lithium batteries in carry-on).</li>
<li>Personal: each shooter handles their own shotgun + ammo per airline rules (TSA-declared, locked hard case, checked), eye/ear protection, overnight bag.</li>
<li>Buy on arrival: wine, water bottles, snacks.</li>
</ul></div>
<div class="rosblock"><h3>Quick contacts</h3><ul class="roslist">
<li>Stacey Holden (Cedar Gate): 405-370-1952 &middot; sholden@thecedargate.com</li>
<li>Michael Pollard (event lead): 678-371-9039</li>
<li>Add day-of cells for David, Elijah, Stephen, Parrish, Lane, Graham, Mitchell, Justin, Chris.</li>
</ul></div>
'''
_OLD_ROS='''
<div class="banner"><b>Updated June 19, 2026.</b> Single source of truth - from leaving the Harbinger office (Tyrone, GA) through the event and back. Items still to confirm are flagged.</div>
<div class="rosblock"><h3>All event links</h3><ul class="roslist">
<li><b>Raffle kiosk</b> (iPad sign-up): <a target="_blank" href="https://cedar-gate-raffle.vercel.app/">cedar-gate-raffle.vercel.app</a></li>
<li><b>Raffle admin</b> (draw winner / export): <a target="_blank" href="https://cedar-gate-raffle.vercel.app/admin">/admin</a></li>
<li><b>Demo booking</b> (Calendly - behind table QR + closing email/text): <a target="_blank" href="https://calendly.com/d/ct7g-x3g-mb5/the-harbinger-demo-okc">Harbinger Demo OKC</a></li>
<li><b>Clay Shoot Evite</b>: <a target="_blank" href="https://evite.me/HarbingerClays">evite.me/HarbingerClays</a></li>
<li><b>Outreach / RSVP sheet</b>: <a target="_blank" href="https://docs.google.com/spreadsheets/d/1O363mPR0ZpvjpsfiJ-3G4XI3LCZS_huZrxk_Mn_W5Pg/edit">Tracker</a></li>
<li><b>Waiver</b> (everyone signs): <a target="_blank" href="https://app.waiversign.com/e/612528c3663fa30019930f0d/doc/61252945663fa30019930fde?eventName=Harbinger%202026">WaiverSign</a></li>
<li><b>Venue</b>: Stacey Holden 405-370-1952 / sholden@thecedargate.com &middot; Abi Hill 405-795-9646 / abi@thecedargate.com</li>
</ul></div>
<div class="rosblock"><h3>Headcounts &amp; food (Stacey/Abi, Jun 17-19)</h3><ul class="roslist">
<li>Thursday dinner at the Lodge: <b>25</b></li>
<li>Friday breakfast (The Wrap): <b>140</b> &middot; Friday lunch (The Chop): <b>140</b></li>
<li>Registration: <b>~35 teams</b></li>
<li>OPEN: team spreadsheet must be filled + returned to the venue (Michael, due Fri)</li>
</ul></div>
<div class="rosblock"><h3>Travel</h3><ul class="roslist">
<li><b>Thursday flight</b> (Delta DL2490, conf# GINV8Z) ATL&rarr;OKC, dep 9:18 AM ET / arr 10:29 AM CT: Michael, Lane, Graham, Stephen, Mitchell, Parrish, Chris Scott (camera).</li>
<li><b>Arriving earlier, own vehicles:</b> Troy, Elijah, David, Justin.</li>
<li>Depart Harbinger (Tyrone, GA) ~6:45 AM (CONFIRM; maybe 6:00 for firearm check). Return Fri ~5:00-5:45 PM (CONFIRM).</li>
<li>2 Hertz rentals (sized for cargo) for the Thursday group.</li>
</ul></div>
<div class="rosblock"><h3>Roles at a glance</h3><ul class="roslist">
<li><b>David Harbin</b> - host; 20-min lunch talk</li>
<li><b>Michael Pollard</b> - logistics lead / quarterback; raffle app + kiosk; runs the day</li>
<li><b>Elijah Lee</b> - registration + lunch setup; partner host</li>
<li><b>Mitchell Attaway</b> - registration + raffle kiosk station (morning sign-ins)</li>
<li><b>Stephen Mitchell</b> - cabin gifts; booth; raffle announce/hype; thanks guests</li>
<li><b>Parrish Walton</b> - cabin gifts; handwritten name tags; FFL gun transfer</li>
<li><b>Lane / Graham / Justin</b> - water-bottle wrapping + cart prep; prospect outreach</li>
<li><b>Chris Scott</b> - camera (shoot, talk, raffle, dinner, team photos)</li>
<li><b>Troy Williams</b> - bourbon pickup (Hoey provides); leads cabin assignments; works prospects</li>
</ul></div>
<div class="rosblock"><h3>Thursday, June 25 - setup &amp; overnight</h3><ul class="roslist">
<li>~2:00 PM - team arrives, sets up (cabin gifts, water bottles, registration + booth, iPad kiosk test+reset, camera)</li>
<li>4:30-5:00 PM - guest cabin check-in</li>
<li><b>5:00 PM - FIVE-STAND COMPETITION (CONFIRMED)</b> - hosts shoot alongside prospects (replaces the Big Gun Experience)</li>
<li>6:30 PM - dinner at the Lodge (25); cigars + wine; spread out, don't cluster</li>
<li>8:00 PM - bourbon tasting / cocktail hour (Hoey's bourbon; Troy picks up)</li>
</ul></div>
<div class="rosblock"><h3>Friday, June 26 - event day (confirmed by Abi, Jun 19)</h3><ul class="roslist">
<li>~7:45 AM - team final setup at the Generations Barn</li>
<li><b>8:30 AM - registration + breakfast (The Wrap)</b>; handwritten name tags (Parrish); raffle entry + name tag = ONE combined iPad station (Mitchell) so every teammate is captured; waiver catch-station</li>
<li>9:45 AM - safety briefing (Cedar Gate staff)</li>
<li><b>10:00 AM - clay shoot</b> - 60 targets, North + South courses; shot 7.5/8/9; ~12 loaner guns ($50/pp) + ammo ($15/box), Harbinger covering; export raffle CSV right after to build the demo list</li>
<li><b>12:00 PM - lunch (The Chop) + David's 20-min talk</b>; at close David invites everyone to book a 10-min demo (table QR)</li>
<li><b>TIMED SEND</b> - as David closes, Michael fires the demo email + text to all registrants + raffle entrants (Luke = backup); goal: phones buzz in the room</li>
<li><b>Raffle draw</b> - Stephen announces/hypes; winner does NOT take the gun on-site - Parrish handles the FFL transfer (in Michael's name, via Stock &amp; Barrel; ATF 4473 + ID + NICS)</li>
<li>Wrap - Stephen thanks guests; lock next steps; export final CSV; teardown; return flight</li>
</ul></div>
<div class="rosblock"><h3>Open items</h3><ul class="roslist">
<li>Team spreadsheet -> return to venue (Michael, due Fri)</li>
<li>Tyrone->ATL departure + return flight time (CONFIRM)</li>
<li>Gun cases + FFL same-day rule (Michael/Parrish; confirm w/ Bass Pro)</li>
<li>Cabin 3 second room TBD (Anna confirming)</li>
<li>Partner-brief meeting - target Friday (Troy flies out Monday)</li>
</ul></div>
<div class="rosblock"><h3>Dress &amp; quick contacts</h3><ul class="roslist">
<li>Dress: boots, polo, jeans (shorts OK). Hot + dusty.</li>
<li>Stacey Holden 405-370-1952 &middot; Abi Hill 405-795-9646 &middot; Michael Pollard 678-371-9039</li>
</ul></div>
'''

TEAMS_SEED={"courses":[
 {"name":"South Course A","teams":[
  {"t":"Team 1A - South (1) - TerraStar","m":["Brad Wittrock","Tiffany Jones","Team Member 3","Team Member 4"]},
  {"t":"Team 2A - South (2) - Summit Technology Group","m":["David Carter","Team Member 2","Team Member 3","Justin Culbertson (Harbinger)"]},
  {"t":"Team 3A - South (3) - Echo Contracting","m":["Kevin Walls","Eddy","Jordan Hayes","Steve Holloway"]},
  {"t":"Team 4A - South (4) - K&C Manufacturing","m":["Kirk Brown","Team Member 2","Elijah Lee (Harbinger)","Shawn Priddy"]},
  {"t":"Team 5A - South (5) - ORCA","m":["Avery Smith","Team Member 2","Team Member 3","Team Member 4"]},
  {"t":"Team 6A - South (6) - Kodiak Gas Services","m":["Joshua Pfeil","Team Member 2","Team Member 3","Team Member 4"]},
  {"t":"Team 7A - South (7) - Dolese Bros.","m":["Derick Miranda","Team Member 2","Team Member 3","Team Member 4 (child)"]},
  {"t":"Team 8A - South (8) - B&H Construction / GES","m":["Scott Munday","Dean Sutterfield","Dean Baker","Jim Bowers"]},
  {"t":"Team 9A - South (9) - B&H Construction (Team 2)","m":["Red Schulze","Team Member 2","Team Member 3","Team Member 4"]},
  {"t":"Team 10A - South (10) - Cultural Discipline","m":["Shawn Priddy","Team Member 2","Team Member 3","Team Member 4"]},
  {"t":"Team 11A - South (11) - Air Technologies","m":["Erik Van Winkle","TJ Green","Team Member 3","Team Member 4"]},
  {"t":"Team 12A - South (12) - The Phoenix Group","m":["Denny Hight","Team Member 2","Team Member 3","Team Member 4"]},
  {"t":"Team 13A - South (13) - The Phoenix Group (Team 2)","m":["Garrett Hight","Justin Adams","Clay Fitzgerald","Gage Wall"]},
  {"t":"Team 14A - South (14) - B&H Construction / GES (Team 2)","m":["Team Member 1","Team Member 2","Team Member 3","Team Member 4"]},
  {"t":"Team 15A - South (15) - (INSERT COMPANY NAME)","m":[]},
 ]},
 {"name":"North Course A","teams":[
  {"t":"Team 1A - North (1) - Company TBD","m":["Anthony Zamora","Team Member 2","Michael Pollard (Harbinger)","Mitchell Attaway (Harbinger)"]},
  {"t":"Team 2A - North (2) - Legacy & Succession","m":["David Chaney","Team Member 2","Team Member 3","Team Member 4"]},
  {"t":"Team 3A - North (3) - Legacy & Succession (Team 2)","m":["David Ortiz","Team Member 2","Team Member 3","Team Member 4"]},
  {"t":"Team 4A - North (4) - Bending Steel (verify company)","m":["Jeremy Bradford","Team Member 2","Team Member 3","Team Member 4"]},
  {"t":"Team 5A - North (5) - Midwest Wrecking","m":["Team Member 1","Team Member 2","Team Member 3","Lane McPherson (Harbinger)"]},
  {"t":"Team 6A - North (6) - Hoey Construction / Southern Lifting","m":["Philip Hoey","Wayne Richards (War Metals)","Colt Hunter (Southern Lifting)","David Harbin (Harbinger)"]},
  {"t":"Team 7A - North (7) - Twisted Oak","m":["Mike Robberson","Scott Stedman","Scott Lemming","Matt Johnson"]},
  {"t":"Team 8A - North (8) - United Systems","m":["Kevin King","Josh Parrish","Graham Turner (Harbinger)","Parrish Walton (Harbinger)"]},
  {"t":"Team 9A - North (9) - Company TBD","m":["Gary Ward","Team Member 2","Team Member 3","Team Member 4"]},
  {"t":"Team 10A - North (10) - FNBT / JPMorgan","m":["John Gorton (FNBT)","Team Member 2","Team Member 3","Stephen Mitchell (Harbinger)"]},
  {"t":"Team 11A - North (11) - MidCentral Energy","m":["Joe Horgan","Team Member 2","Team Member 3","Team Member 4"]},
  {"t":"Team 12A - North (12) - Jimmie Dean Foundation","m":["Robert Boyd","Team Member 2","Team Member 3","Team Member 4"]},
  {"t":"Team 13A - North (13) - KLX Energy (verify company)","m":["Allen Strider","Team Member 2","Team Member 3","Team Member 4"]},
  {"t":"Team 14A - North (14) - (INSERT COMPANY NAME)","m":[]},
  {"t":"Team 15A - North (15) - (INSERT COMPANY NAME)","m":[]},
 ]},
 {"name":"South Course B","teams":[{"t":"Team "+str(_n)+" - South ("+str(_n-15)+") - (INSERT COMPANY NAME)","m":[]} for _n in range(16,31)]},
 {"name":"North Course B","teams":[{"t":"Team "+str(_n)+" - North ("+str(_n-15)+") - (INSERT COMPANY NAME)","m":[]} for _n in range(16,31)]},
]}

TEAMS_HTML=('''
<div class="banner"><b>Shoot Team Assignments</b> &mdash; drag a person between teams, click any name or team title to edit it, and use <b>+ person</b> / <b>+ Add team</b> to grow a course. Edits save automatically and sync to the team. <span id="teamstatus" class="twarn">Loading&hellip;</span></div>
<div class="tbtns"><button class="tbtn" onclick="window.__teamsExport()">Export JSON</button> <button class="tbtn danger" onclick="window.__teamsReset()">Reset to defaults</button></div>
<div id="teamsroot"></div>
<style>
.tbtns{margin:0 0 12px}
.tbtn{font-size:12px;font-weight:700;border:1px solid #cfd6df;background:#fff;border-radius:8px;padding:6px 12px;cursor:pointer;color:#1f3a5f;margin-right:6px}
.tbtn.danger{color:#a23}
#teamstatus{font-size:12px;font-weight:700;margin-left:6px}
.tok{color:#1a7f4b}.twarn{color:#b06a00}
.tcourse{margin-bottom:22px}
.tcourse-h{font-size:14px;font-weight:800;color:#1f3a5f;background:#eef2f7;border:1px solid #dde4ec;border-radius:8px;padding:7px 12px;margin-bottom:10px}
.tgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(235px,1fr));gap:10px}
.tcard{background:#fff;border:1px solid #e2e7ee;border-radius:10px;padding:10px;min-height:90px}
.tcard.drop{border-color:#1f3a5f;box-shadow:0 0 0 2px rgba(31,58,95,.25)}
.tt{font-weight:700;font-size:12.5px;color:#16202c;border-bottom:1px dashed #e2e7ee;padding-bottom:6px;margin-bottom:7px;outline:none}
.tchip{display:flex;align-items:center;gap:6px;background:#f4f6f9;border:1px solid #e2e7ee;border-radius:7px;padding:4px 7px;margin-bottom:5px;cursor:grab}
.tchip:active{cursor:grabbing}
.tnm{flex:1;font-size:12.5px;color:#1d2733;outline:none}
.tx{border:none;background:transparent;color:#b0808a;font-size:14px;line-height:1;cursor:pointer;padding:0 2px}
.tadd{font-size:11px;font-weight:700;color:#1f6b6b;background:#eef6f6;border:1px dashed #bcd;border-radius:6px;padding:3px 8px;cursor:pointer;margin-top:3px}
.tdel{display:block;margin-top:7px;font-size:10.5px;color:#a23;background:transparent;border:none;cursor:pointer}
.taddteam{margin-top:10px;font-size:12px;font-weight:700;color:#1f3a5f;background:#fff;border:1px dashed #9bb;border-radius:8px;padding:6px 12px;cursor:pointer}
</style>
'''
+ '<script>window.__TEAMSEED=' + json.dumps(TEAMS_SEED) + ';</script>'
+ '''<script>
(function(){
 var KEY="cedargate_teams_v1"; var seed=window.__TEAMSEED;
 var STATE=null, saveTimer=null, lastServer=0, editing=false;
 function loadLocal(){try{var s=localStorage.getItem(KEY);if(s)return JSON.parse(s);}catch(e){}return null;}
 function persistLocal(){try{localStorage.setItem(KEY,JSON.stringify(STATE));}catch(e){}}
 function setStatus(t,cls){var el=document.getElementById("teamstatus");if(el){el.textContent=t;el.className=cls||"";}}
 function serverLoad(cb){fetch("/api/teams",{cache:"no-store"}).then(function(r){return r.ok?r.json():null;}).then(function(d){cb(d&&d.courses?d:null);}).catch(function(){cb(null);});}
 function serverSave(){STATE.updated=Date.now();fetch("/api/teams",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(STATE)}).then(function(r){if(r.ok){lastServer=STATE.updated;setStatus("Saved & synced ✓","tok");}else{setStatus("Saved on this device (team sync not connected)","twarn");}}).catch(function(){setStatus("Saved on this device (team sync not connected)","twarn");});}
 function save(){persistLocal();setStatus("Saving…","");clearTimeout(saveTimer);saveTimer=setTimeout(serverSave,600);}
 function render(){
  var root=document.getElementById("teamsroot");if(!root)return;root.innerHTML="";
  STATE.courses.forEach(function(course,ci){
   var sec=document.createElement("div");sec.className="tcourse";
   var h=document.createElement("div");h.className="tcourse-h";h.textContent=course.name;sec.appendChild(h);
   var grid=document.createElement("div");grid.className="tgrid";
   course.teams.forEach(function(team,ti){
    var card=document.createElement("div");card.className="tcard";
    card.addEventListener("dragover",function(e){e.preventDefault();card.classList.add("drop");});
    card.addEventListener("dragleave",function(){card.classList.remove("drop");});
    card.addEventListener("drop",function(e){e.preventDefault();card.classList.remove("drop");onDrop(e,ci,ti);});
    var tt=document.createElement("div");tt.className="tt";tt.contentEditable=true;tt.textContent=team.t;
    tt.addEventListener("focus",function(){editing=true;});tt.addEventListener("blur",function(){editing=false;team.t=tt.textContent.trim();save();});
    card.appendChild(tt);
    team.m.forEach(function(name,mi){
     var chip=document.createElement("div");chip.className="tchip";chip.draggable=true;
     chip.addEventListener("dragstart",function(e){e.dataTransfer.setData("text/plain",ci+","+ti+","+mi);e.dataTransfer.effectAllowed="move";});
     var span=document.createElement("span");span.className="tnm";span.contentEditable=true;span.textContent=name;
     span.addEventListener("focus",function(){editing=true;});span.addEventListener("blur",function(){editing=false;team.m[mi]=span.textContent.trim();save();});
     var del=document.createElement("button");del.className="tx";del.textContent="×";del.title="Remove";
     del.addEventListener("click",function(){team.m.splice(mi,1);save();render();});
     chip.appendChild(span);chip.appendChild(del);card.appendChild(chip);
    });
    var add=document.createElement("button");add.className="tadd";add.textContent="+ person";
    add.addEventListener("click",function(){team.m.push("New person");save();render();});
    card.appendChild(add);
    var delT=document.createElement("button");delT.className="tdel";delT.textContent="Delete team";
    delT.addEventListener("click",function(){if(confirm("Delete this team?")){course.teams.splice(ti,1);save();render();}});
    card.appendChild(delT);
    grid.appendChild(card);
   });
   var addT=document.createElement("button");addT.className="taddteam";addT.textContent="+ Add team";
   addT.addEventListener("click",function(){course.teams.push({t:"New Team - (INSERT COMPANY NAME)",m:[]});save();render();});
   sec.appendChild(grid);sec.appendChild(addT);root.appendChild(sec);
  });
 }
 function onDrop(e,ci,ti){var d=e.dataTransfer.getData("text/plain");if(!d)return;var p=d.split(",").map(Number);var fc=p[0],ft=p[1],fm=p[2];if(fc===ci&&ft===ti)return;var nm=STATE.courses[fc].teams[ft].m[fm];if(nm===undefined)return;STATE.courses[fc].teams[ft].m.splice(fm,1);STATE.courses[ci].teams[ti].m.push(nm);save();render();}
 function start(){serverLoad(function(server){var local=loadLocal();if(server){STATE=server;lastServer=server.updated||0;setStatus("Synced with team ✓","tok");}else if(local&&local.courses){STATE=local;setStatus("Saved on this device (team sync not connected)","twarn");}else{STATE=JSON.parse(JSON.stringify(seed));STATE.updated=0;setStatus("Showing defaults","twarn");}render();setInterval(poll,15000);});}
 function poll(){if(editing)return;serverLoad(function(server){if(server&&(server.updated||0)>lastServer){STATE=server;lastServer=server.updated;render();setStatus("Updated from team ✓","tok");}});}
 window.__teamsExport=function(){var blob=new Blob([JSON.stringify(STATE,null,2)],{type:"application/json"});var a=document.createElement("a");a.href=URL.createObjectURL(blob);a.download="cedar-gate-teams.json";a.click();};
 window.__teamsReset=function(){if(confirm("Reset to the original seeded teams? This clears edits.")){STATE=JSON.parse(JSON.stringify(seed));STATE.updated=Date.now();save();render();}};
 if(document.readyState!=="loading")start();else document.addEventListener("DOMContentLoaded",start);
})();
</script>''')

HTML=f'''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>Cedar Gate Connection Cheat Sheet</title>
<style>
:root{{color-scheme:light}}
*{{box-sizing:border-box}}
body{{margin:0;background:#f4f6f9;color:#1d2733;font-family:-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif}}
.wrap{{max-width:1180px;margin:0 auto;padding:18px}}
h1{{font-size:22px;margin:0 0 2px;color:#1f3a5f}}
.sub{{color:#5b6675;font-size:13px;margin:0 0 14px}}
.tabs{{display:flex;gap:8px;margin-bottom:16px;flex-wrap:wrap}}
.tab{{padding:10px 16px;border:1px solid #cfd6df;background:#fff;border-radius:9px;cursor:pointer;font-weight:600;font-size:14px;color:#1f3a5f}}
.tab.active{{background:#1f3a5f;color:#fff;border-color:#1f3a5f}}
.page{{display:none}}
.page.active{{display:block}}
.banner{{background:#eef2f7;border:1px solid #dde4ec;border-radius:9px;padding:10px 14px;font-size:13px;color:#43505f;margin-bottom:14px}}
.repgroup{{margin-bottom:22px}}
.repgroup h3{{font-size:15px;margin:0 0 10px;padding:5px 0 5px 12px}}
.cnt{{background:#e6ebf1;color:#43505f;border-radius:20px;padding:1px 9px;font-size:12px;margin-left:6px;vertical-align:middle}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(330px,1fr));gap:12px}}
.card{{background:#fff;border:1px solid #e2e7ee;border-radius:11px;padding:13px 14px;box-shadow:0 1px 2px rgba(20,40,70,.05)}}
.cardtop{{display:flex;gap:11px;align-items:center}}
.av{{width:46px;height:46px;border-radius:50%;color:#fff;font-weight:700;font-size:16px;display:flex;align-items:center;justify-content:center;flex:0 0 auto}}
.avlink{{position:relative;text-decoration:none;display:block}}
.cam{{position:absolute;bottom:-4px;left:50%;transform:translateX(-50%);background:#1f3a5f;color:#fff;font-size:8px;font-weight:700;padding:1px 5px;border-radius:7px;letter-spacing:.3px}}
.avwrap{{flex:0 0 auto;display:block}}
.avimg{{width:46px;height:46px;border-radius:50%;object-fit:cover;display:block;border:1px solid #e2e7ee}}
.fit{{margin:3px 0 6px}}
.stars{{color:#e0a500;font-size:14px;letter-spacing:1px}}
.stars .off{{color:#d4dae2}}
.nm{{font-weight:700;font-size:15px;color:#16202c;line-height:1.15}}
.co{{font-size:12.5px;color:#5b6675;margin-top:1px}}
.chips{{margin:9px 0 7px;display:flex;flex-wrap:wrap;gap:5px}}
.chip{{font-size:10.5px;font-weight:700;padding:2px 7px;border-radius:20px;color:#fff;letter-spacing:.2px}}
.chip.role{{background:#5b6675}}
.chip.unc{{background:#b06a00}}
.chip.ov{{background:#2a5d8f}}
.chip.cl{{background:#1a7f4b}}
.meta{{font-size:12px;color:#43505f;margin-bottom:5px}}
.links{{font-size:12px}}
.links a{{color:#1155cc;text-decoration:none}}
.muted{{color:#9aa4b1}}
.note{{margin-top:7px;font-size:11.5px;color:#6b7785;font-style:italic;border-top:1px dashed #e2e7ee;padding-top:6px}}
.foot{{color:#8893a1;font-size:11px;margin-top:18px;text-align:center}}
.rosblock{{background:#fff;border:1px solid #e2e7ee;border-radius:11px;padding:12px 16px;margin-bottom:12px}}
.rosblock h3{{margin:0 0 8px;font-size:15px;color:#1f3a5f;border-left:6px solid #1f3a5f;padding-left:10px}}
.roslist{{margin:0;padding-left:18px}}
.roslist li{{font-size:13px;color:#384350;margin-bottom:5px;line-height:1.4}}
.roslist a{{color:#1155cc;text-decoration:none}}
</style></head>
<body><div class="wrap">
<h1>Cedar Gate Clay Shoot - Connection Cheat Sheet</h1>
<p class="sub">Harbinger Marketing &middot; The Cedar Gate, Kingfisher OK &middot; Thu Jun 25 (overnight) - Fri Jun 26 (shoot). Tap an avatar marked <b>photo</b> for the face; tap LinkedIn/Website for more.<br><b>Best-fit stars (1-5)</b> rate match to Harbinger's ICP (OK trades, construction, home-services, manufacturing, energy-services) - existing clients &amp; core trades score highest; enterprises, banks, nonprofits &amp; associations score lower.</p>
<div class="tabs">
 <div class="tab active" onclick="show('ov',this)">Overnight - Thursday</div>
 <div class="tab" onclick="show('sh',this)">Shoot Day - Friday</div>
 <div class="tab" onclick="show('ros',this)">Run of Show</div>
 <div class="tab" onclick="show('cab',this)">Cabins</div>
 <div class="tab" onclick="show('teams',this)">Shoot Teams</div>
</div>

<div id="ov" class="page active">
 <div class="banner"><b>Thursday overnight stay</b> - dinner, five-stand, bourbon at the cabins. Everyone here is also at Friday's shoot. <b>Current Partners</b> (existing clients) are grouped first - relationship time, no prospecting rep. New prospects show their assigned Harbinger host.</div>
 {overnight_html}
</div>

<div id="sh" class="page">
 <div class="banner"><b>Friday shoot - confirmed attendees</b>, grouped by the Harbinger host who owns the connection. Confirmed guests sit with their host (Troy, Elijah, or Stephen); Graham's and Lane's invitees move to a host only once they RSVP yes - until then they're listed under Graham/Lane in the Unconfirmed section below. Troy &amp; Chris don't shoot - Troy greets/owns only; support staff fill open squad seats.</div>
 {shoot_conf_html}
 <h2 style="font-size:16px;color:#b06a00;margin:26px 0 6px">Still chasing - invited, not yet confirmed</h2>
 <div class="banner" style="background:#fdf6ec;border-color:#f0e0c8"><b>These still need to be confirmed</b> - listed under the rep who invited them (<b>Lane</b> or <b>Graham</b>) so they know to chase the RSVP. Once a guest confirms yes, they move to their assigned host (Troy, Elijah, or Stephen).</div>
 {shoot_unc_html}
</div>

<div id="ros" class="page">{RUNOFSHOW_HTML}</div>
<div id="cab" class="page">{CABINS_HTML}</div>
<div id="teams" class="page">{TEAMS_HTML}</div>

<div class="foot">Counts verified against the live Evite (Yes = 96) on Jun 19, 2026. Links double-verified. Photos link out to public sources (sandbox can't embed images inline).</div>
</div>
<script>
function imgFail(el){{el.style.display='none';el.nextElementSibling.style.display='flex';}}
function show(id,el){{
 document.querySelectorAll('.page').forEach(p=>p.classList.remove('active'));
 document.getElementById(id).classList.add('active');
 document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));
 el.classList.add('active');
 window.scrollTo(0,0);
}}
</script>
</body></html>'''

import os
out=os.path.join(os.getcwd(), "cedar_gate_cheatsheet_photos.html" if IMG_MODE else "cedar_gate_cheatsheet.html")
open(out,"w").write(HTML)
print("WROTE",out,len(HTML),"bytes")
