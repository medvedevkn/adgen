pg_conn = {
# {db connection}
}

redis_conn = {
# {redis connection}
}

query = "SELECT DISTINCT API_KEY FROM public.buyer where status = 'active';"

query_buyer = "SELECT DISTINCT id FROM public.buyer where status = 'active';"

query_gen = "SELECT max(query_id) from public.query;"

query_gen_update = "insert into public.query (query_id, buyer_id, keyword, event_dt) values (%s, %s, %s, %s);"

gen_insert = "insert into public.generations (query_id, model_id, keyword, buyer_id, response, gen_dt) values (%s, %s, %s, %s, %s, %s);"

gen_result = "select distinct response from public.v_generations where query_id = %s"

time_spent = "select avg(t.timedif)::int from (select extract(seconds from t1.gen_dt::timestamp - t2.event_dt::timestamp) as timedif \
from public.v_generations t1 \
join public.query t2 \
on t1.query_id = t2.query_id \
order by t1.query_id desc \
limit 3) t \
"

feed_insert = "insert into public.feedback (query_id, value) values (%s, %s);"

#url = # {model service url}

post_query = '''
    curl -X 'POST' \
    -H 'accept: text/plain' \
    -H 'Content-Type: application/json' \
    -d '{
    "text": "[INST] As a professional mediabuyer create 3 ad titles for keyword %s. limit is 50 words [/INST]"
    }'
    '''


post_q = {
    'accept': 'text/plain',
    'Content-Type': 'application/json',
    "text": ""
}

def handle_prompt(keyword):
    if keyword.lower().find('t:') == 0:
        return "[INST] As a professional mediabuyer create 3 ad titles for keyword {} without emoji, hashtags brand names, notes for 40 symbols[/INST]".format(keyword[2:])
    if keyword.lower().find('c:') == 0:
        return "[INST] As a professional mediabuyer create 3 ad creatives for keyword {} without emoji, hashtags, brand names, notes for 90 symbols[/INST]".format(keyword[2:])
    return "[INST] {} [/INST]".format(keyword)  

