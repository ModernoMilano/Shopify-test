"""Real delivery times (owner, 2026-11-04): dispatched within 1 business day, delivered in 3-5 business days.
Updates the shipping page, FAQ, product-page shipping texts (all product templates) and product_templates.py source.
(The product-page estimate is in delivery_eta.py, the cart notes and the Christmas order-by date in bfcm/.)"""
import re, json
from lib import gql, check, theme_file, put_theme_files, THEME

def page(handle):
    return gql('query($q:String!){pages(first:2,query:$q){nodes{id body}}}', {"q": f"handle:{handle}"})["pages"]["nodes"][0]
def save(p, body):
    print(check(gql("mutation($id:ID!,$p:PageUpdateInput!){pageUpdate(id:$id,page:$p){page{id} userErrors{field message}}}",
                    {"id": p["id"], "p": {"body": body}})["pageUpdate"]))

# shipping page
p = page("shipping"); b = p["body"]
b = re.sub(r"Orders are prepared and dispatched within 1(–|&ndash;)3 business days",
           "Orders are dispatched within 1 business day", b)
b = re.sub(r"<table.*?</table>", "<p><strong>Delivered in 3&ndash;5 business days</strong>, with tracking on every order.</p>", b, flags=re.S)
b = b.replace("The product page shows where an item ships from. ", "").replace("The product page shows where an item ships from.", "")
save(p, b)

# FAQ
p = page("faq"); b = p["body"]
b2 = re.sub(r"Orders are prepared within 1(–|&ndash;)3 business days\.(.*?)Delivery across the United States typically takes a further 5(–|&ndash;)12 business days\.",
            r"Orders are dispatched within 1 business day.\2Delivery takes 3&ndash;5 business days.", b, flags=re.S)
print("faq changed:", b2 != b); save(p, b2)

# product templates
R = [("Dispatched in 1&ndash;3 business days with tracking. Delivery across the US in 5&ndash;12 business days.",
      "Dispatched within 1 business day with tracking. Delivered in 3&ndash;5 business days."),
     ("Orders are prepared in 1&ndash;3 business days and delivered across the US in 5&ndash;12 business days",
      "Orders are dispatched within 1 business day and delivered in 3&ndash;5 business days"),
     ("Prepared within 1&ndash;3 business days and shipped with tracking on every order: delivery across the US in 5&ndash;12 business days.",
      "Dispatched within 1 business day and shipped with tracking on every order: delivered in 3&ndash;5 business days.")]
names = [n["filename"] for n in gql('query($id:ID!){theme(id:$id){files(first:50,filenames:["templates/product*.json"]){nodes{filename}}}}',
                                    {"id": THEME})["theme"]["files"]["nodes"]]
files = {}
for n in names:
    c = theme_file(n); c2 = c
    for a, z in R: c2 = c2.replace(a, z)
    if c2 != c: files[n] = c2
put_theme_files(files); print("templates:", list(files))
src = open("product_templates.py").read()
for a, z in R: src = src.replace(a, z)
open("product_templates.py", "w").write(src)
