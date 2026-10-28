import sys, os
S = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, S)
from lib import gql, check

# Business details still to be filled in by the owner (shown to customers until replaced).
CO = "ModernoMilano"
ADDR = "Midden Geestweg 4, 1861 VG Bergen, the Netherlands"
KVK = "81346034"
VAT = "NL003553643B29"
EMAIL = '<a href="mailto:info@modernomilano.com">info@modernomilano.com</a>'
PHONE = "+31 6 83907658"
UPDATED = "October 28, 2026"
CONTACT = '<a href="/pages/contact">contact page</a>'

PAGES = {}

PAGES["about"] = ("Our Story", f"""
<p><em>CozyCompanion was born from a simple belief: the best moments at home are the quiet ones.</em></p>
<p>A soft blanket at the end of a long day. Warm light, a good book, a cup of tea. A companion curled up beside you, breathing slowly, perfectly content. These are the moments that make a house feel like home &mdash; and the ones we design for.</p>
<h2>Luxury, the gentle kind</h2>
<p>To us, luxury isn't loud. It's the feeling of fabric that's genuinely soft, warmth that arrives exactly when you want it, and technology that quietly takes care of things so you don't have to. We curate every piece in our collection around that idea: considered, beautiful, and made to be used every day.</p>
<h2>For you, and for them</h2>
<p>Our pets are family. That's why our collection brings together two worlds that belong together: <a href="/collections/cozy-heated-blankets">heated blankets</a> for cozy evenings, and <a href="/collections/smart-pet-tech">smart pet essentials</a> that keep your companions fed, hydrated, warm and close &mdash; even when you can't be there.</p>
<h2>Our promise</h2>
<ul>
<li><strong>Thoughtfully curated</strong> &ndash; we only offer pieces we would happily give to the people (and pets) we love.</li>
<li><strong>30-day happiness guarantee</strong> &ndash; if it doesn't feel right, return it. <a href="/pages/returns">See how returns work</a>.</li>
<li><strong>Real people, real care</strong> &ndash; questions before or after your order? Reach us any time through our {CONTACT}.</li>
</ul>
<p>Thank you for welcoming us into your home.</p>
<p><em>&mdash; The CozyCompanion team</em></p>
""")

PAGES["faq"] = ("Frequently Asked Questions", f"""
<h2>Orders &amp; shipping</h2>
<h3>How long will my order take to arrive?</h3>
<p>Orders are prepared within 1&ndash;3 business days. We ship worldwide with tracking. Delivery across the United States typically takes a further 5&ndash;12 business days. You'll find the full details on our <a href="/pages/shipping">shipping page</a>.</p>
<h3>Will I receive a tracking number?</h3>
<p>Yes. As soon as your order ships, you'll receive an email with your tracking link so you can follow it all the way to your door.</p>
<h3>Can my order arrive in more than one parcel?</h3>
<p>Occasionally, yes. If you order several items, they may be shipped separately so that each arrives as quickly as possible. Each parcel has its own tracking link.</p>
<h3>Can I change or cancel my order?</h3>
<p>Contact us as soon as possible through our {CONTACT}. If your order hasn't been processed yet, we'll gladly change or cancel it.</p>

<h2>Returns &amp; guarantee</h2>
<h3>What is your return policy?</h3>
<p>You can return any item within 30 days of delivery under our happiness guarantee, provided it is unused and in its original packaging. Read our <a href="/pages/returns">returns &amp; refunds policy</a> for the full details.</p>
<h3>What if my item arrives damaged or faulty?</h3>
<p>We're so sorry if that happens. Contact us within 14 days of delivery with your order number and a photo of the issue, and we'll arrange a replacement or full refund at no cost to you.</p>

<h2>Heated blankets</h2>
<h3>How do I care for my heated blanket?</h3>
<p>Always follow the care label and instructions included with your blanket. Before washing, disconnect the controller and power cable. Many of our blankets are machine washable on a gentle, cool cycle; never iron, dry-clean or tumble-dry on high heat unless the label says it's safe.</p>
<h3>Can I use a heated blanket every night?</h3>
<p>Heated blankets are designed for everyday comfort. For safe use, follow the instructions included with your product, don't fold or bunch the blanket while it's switched on, and switch it off when it isn't in use.</p>
<h3>Is the pet heated blanket suitable for all pets?</h3>
<p>It's designed for cats and dogs, and is especially loved by senior pets, small breeds and short-coated companions. Always supervise pets who like to chew, and make sure they can move off the blanket if they become too warm.</p>

<h2>Smart pet tech</h2>
<h3>Do the smart feeders and tracker need an app?</h3>
<p>Smart features are set up through the companion app described in the instructions included with your device. Basic setup takes just a few minutes.</p>

<h2>Payment &amp; discounts</h2>
<h3>Which payment methods do you accept?</h3>
<p>We accept all major credit and debit cards, plus the express payment options shown at checkout. Every payment is processed through a secure, encrypted checkout. All prices are in US dollars.</p>
<h3>How do I use my discount code?</h3>
<p>Enter your code in the discount field at checkout. Our Bundle &amp; Save offer (10% off when you buy 2 or more items) is applied automatically in your cart.</p>

<h2>Still have a question?</h2>
<p>We're happy to help. Send us a message through our {CONTACT} and we'll get back to you within 1&ndash;2 business days.</p>
""")

PAGES["shipping"] = ("Shipping Policy", f"""
<p><em>Last updated: {UPDATED}</em></p>
<h2>Processing time</h2>
<p>Orders are prepared and dispatched within 1&ndash;3 business days (Monday to Friday, excluding public holidays). During busy periods such as the holiday season, please allow a little extra time.</p>
<h2>Tracked delivery across the US</h2>
<p>We ship to all 50 states, and every order is sent with tracking.</p>
<table>
<thead><tr><th>Ships from</th><th>Estimated delivery after dispatch</th></tr></thead>
<tbody>
<tr><td>Our US warehouse</td><td>3&ndash;7 business days</td></tr>
<tr><td>Our international warehouses</td><td>7&ndash;12 business days</td></tr>
</tbody>
</table>
<p>The product page shows where an item ships from.</p>
<p>Delivery times are estimates and not guaranteed; they may vary due to carrier delays, customs or circumstances beyond our control.</p>
<h2>Shipping costs</h2>
<p>Shipping costs are calculated and shown at checkout before you pay. Any free-shipping offers are clearly displayed in the store and at checkout.</p>
<h2>Multiple parcels</h2>
<p>Some products are shipped from different warehouses. If you order several items, you may receive them in separate parcels, at no extra cost to you.</p>
<h2>Tracking</h2>
<p>Once your order has shipped, you'll receive a confirmation email with a tracking link. Tracking can take up to 48 hours to show its first update.</p>
<h2>Customs &amp; duties</h2>
<p>US orders are sent with any import duties handled by us. You should never be asked to pay a fee on delivery; if a carrier ever asks you to, please contact us before paying and we'll sort it out.</p>
<h2>Lost or delayed parcels</h2>
<p>If your tracking hasn't updated for 7 business days, or your parcel hasn't arrived within the estimated time, please contact us through our {CONTACT}. We'll investigate with the carrier and make it right.</p>
<h2>Incorrect address</h2>
<p>Please double-check your shipping address at checkout. If you notice a mistake, contact us immediately; we can update it as long as the order hasn't been dispatched.</p>
""")

PAGES["returns"] = ("Returns & Refunds", f"""
<p><em>Last updated: {UPDATED}</em></p>
<h2>Our 30-day happiness guarantee</h2>
<p>We want you to love every piece. If you're not completely happy, you can return your item within <strong>30 days of delivery</strong> for a full refund of the purchase price.</p>
<h2>Conditions</h2>
<ul>
<li>Items must be unused, unwashed and returned in their original packaging, including all accessories, controllers and cables.</li>
<li>You may handle and inspect the product as you would in a shop. If an item shows wear or damage beyond that, we may deduct an amount for the reduced value.</li>
<li>Gift cards are not refundable.</li>
</ul>
<h2>How to return an item</h2>
<ol>
<li>Contact us through our {CONTACT} within 30 days of delivery, stating your order number and the item(s) you'd like to return. </li>
<li>We'll reply within 1&ndash;2 business days with your return address and instructions. Please do not send items back without contacting us first, as returns may go to a different address than the one they were shipped from.</li>
<li>Pack the item securely and send it back within 14 days of contacting us. We recommend a tracked shipping service.</li>
</ol>
<h2>Return shipping costs</h2>
<p>Unless the item is damaged, faulty or incorrect, the cost of returning it is paid by you.</p>
<h2>Refunds</h2>
<p>Once your return arrives and has been checked, we refund the purchase price within 5&ndash;10 business days. Refunds are made using the same payment method you used for your order.</p>
<h2>Damaged, faulty or incorrect items</h2>
<p>If your item arrives damaged, faulty or isn't what you ordered, contact us within 14 days of delivery with your order number and photos. We'll send a replacement or issue a full refund, and you won't pay anything for the return.</p>
<h2>Warranty</h2>
<p>If a defect that was present at delivery appears within 12 months, contact us and we'll repair, replace or refund the item. This does not limit any rights you have under the law of your state.</p>
""")

PAGES["privacy-policy"] = ("Privacy Policy", f"""
<p><em>Last updated: {UPDATED}</em></p>
<p>This privacy policy explains how {CO}, operating under the trade name CozyCompanion ("CozyCompanion", "we", "us"), collects and uses your personal data when you visit or purchase from our store. As a company based in the Netherlands, we process personal data in accordance with the EU General Data Protection Regulation (GDPR), which gives every customer, wherever they live, the protections described below.</p>
<h2>Who is responsible</h2>
<p>{CO}, {ADDR}. Chamber of Commerce (KvK): {KVK}. Contact: {EMAIL} or our {CONTACT}.</p>
<h2>What data we collect</h2>
<ul>
<li><strong>Order data:</strong> name, shipping and billing address, email address, phone number (if provided), products ordered and payment status. We do not store your full payment card details.</li>
<li><strong>Account data:</strong> if you create an account, your login details and order history.</li>
<li><strong>Communication data:</strong> messages you send us via the contact form or email.</li>
<li><strong>Newsletter data:</strong> your email address and your consent, if you subscribe.</li>
<li><strong>Device and usage data:</strong> IP address, browser type, pages viewed and similar information collected through cookies.</li>
</ul>
<h2>Why we use your data, and on what legal basis</h2>
<ul>
<li>To process, ship and support your order (performance of a contract).</li>
<li>To comply with legal obligations such as tax and accounting rules (legal obligation).</li>
<li>To send our newsletter and offers (your consent, which you can withdraw at any time via the unsubscribe link).</li>
<li>To keep our store secure, prevent fraud and improve our website (legitimate interest).</li>
<li>To measure and personalize advertising, only where you have given consent through the cookie banner.</li>
</ul>
<h2>Who we share data with</h2>
<p>We only share data where necessary to run our store, with:</p>
<ul>
<li>Shopify, our e-commerce platform and hosting provider;</li>
<li>payment providers that process your payment securely;</li>
<li>our fulfilment partners and suppliers, and shipping carriers, who prepare and deliver your order;</li>
<li>email and marketing tools, if you have subscribed or consented;</li>
<li>authorities, where we are legally required to do so.</li>
</ul>
<p>Some of these providers may process data outside the European Economic Area. Where this happens, we ensure appropriate safeguards are in place, such as the European Commission's Standard Contractual Clauses.</p>
<h2>How long we keep your data</h2>
<p>We keep order and invoice data for 7 years to meet our legal tax obligations. Other data is kept only as long as necessary for the purpose it was collected for, or until you withdraw your consent.</p>
<h2>Cookies</h2>
<p>We use necessary cookies to make our store work (for example, your cart). Analytics and marketing cookies are only placed with your consent, which you can manage through the cookie banner.</p>
<h2>Your rights</h2>
<p>You have the right to access, correct, delete or restrict the processing of your personal data, to object to processing, and to data portability. To exercise these rights, contact us through our {CONTACT}. You also have the right to lodge a complaint with the Dutch Data Protection Authority (Autoriteit Persoonsgegevens).</p>
<h2>US residents</h2>
<p>We do not sell your personal information. Residents of California and other US states with privacy laws may request access to, correction of, or deletion of their personal information, and may opt out of targeted advertising, by contacting us through our {CONTACT}. We will not discriminate against you for exercising these rights.</p>
<h2>Changes</h2>
<p>We may update this policy from time to time. The latest version will always be available on this page.</p>
""")

PAGES["terms-of-service"] = ("Terms of Service", f"""
<p><em>Last updated: {UPDATED}</em></p>
<h2>1. About us</h2>
<p>This online store is operated under the trade name CozyCompanion by {CO}, {ADDR}, Chamber of Commerce (KvK) {KVK}, VAT {VAT}, email {EMAIL} ("CozyCompanion", "we", "us"). These terms apply to every offer and every order placed in our store.</p>
<h2>2. Offers and prices</h2>
<p>All prices are in US dollars ($). Shipping costs and any applicable sales tax are shown at checkout before you place your order. We make every effort to describe and display our products accurately; images are for illustration and colors may vary slightly depending on your screen. Obvious mistakes or errors in an offer do not bind us.</p>
<h2>3. Ordering and the contract</h2>
<p>The contract is concluded when you complete your order and receive our order confirmation by email. We may refuse or cancel an order in case of suspected fraud, stock unavailability or an obvious pricing error; any payment made will then be refunded in full.</p>
<h2>4. Payment</h2>
<p>Payment is made at checkout through the payment methods offered. Your order is processed once payment has been received.</p>
<h2>5. Delivery</h2>
<p>We deliver to the address you provide. Delivery times are estimates; see our <a href="/pages/shipping">shipping policy</a>. If delivery is delayed by more than 30 days, you may cancel the order free of charge. The risk of loss or damage passes to you upon delivery.</p>
<h2>6. Returns</h2>
<p>You may return your purchase within 30 days of delivery under our happiness guarantee. Conditions are set out in our <a href="/pages/returns">returns &amp; refunds policy</a>.</p>
<h2>7. Guarantee and conformity</h2>
<p>Our products meet the agreement and the specifications stated in the offer. Our warranty is described in our <a href="/pages/returns">returns &amp; refunds policy</a> and does not limit any rights you have under applicable law.</p>
<h2>8. Product use</h2>
<p>Please use all products, in particular electrical products such as heated blankets and smart devices, in accordance with the instructions supplied with them.</p>
<h2>9. Liability</h2>
<p>Our liability is limited to the amount of the order concerned, except in cases of intent or gross negligence, or where liability cannot be limited by law.</p>
<h2>10. Complaints</h2>
<p>Complaints can be submitted through our {CONTACT}. We aim to respond within 14 days.</p>
<h2>11. Governing law</h2>
<p>These terms are governed by Dutch law. This does not affect any mandatory consumer protection laws of the state or country where you live.</p>
""")

PAGES["legal-notice"] = ("Legal Notice", f"""
<p><strong>CozyCompanion</strong> is a trade name of:</p>
<p>{CO}<br>{ADDR}<br>Chamber of Commerce (KvK): {KVK}<br>VAT number: {VAT}<br>Email: {EMAIL}<br>Phone: {PHONE}</p>
<p>For questions about orders, please use our {CONTACT}.</p>
""")

existing = {p["handle"]: p["id"] for p in gql("{ pages(first:50){nodes{id handle}} }")["pages"]["nodes"]}
for handle, (title, body) in PAGES.items():
    page = {"title": title, "body": body.strip(), "isPublished": True}
    if handle in existing:
        r = gql("mutation($id:ID!,$p:PageUpdateInput!){pageUpdate(id:$id,page:$p){page{handle} userErrors{field message}}}",
                {"id": existing[handle], "p": page})["pageUpdate"]
    else:
        page["handle"] = handle
        r = gql("mutation($p:PageCreateInput!){pageCreate(page:$p){page{handle} userErrors{field message}}}", {"p": page})["pageCreate"]
    check(r, handle); print("page ok:", r["page"]["handle"])

# Contact page intro (the theme renders the form below the body)
cid = existing.get("contact")
if cid:
    body = ("<p>We'd love to hear from you. Whether you have a question about a product, your order or a return, "
            "send us a message below and we'll get back to you within 1&ndash;2 business days.</p>"
            "<p>Before you write, you may find your answer in our <a href=\"/pages/faq\">FAQ</a>.</p>")
    check(gql("mutation($id:ID!,$p:PageUpdateInput!){pageUpdate(id:$id,page:$p){page{handle} userErrors{field message}}}",
              {"id": cid, "p": {"title": "Contact us", "body": body}})["pageUpdate"], "contact")
    print("page ok: contact")
