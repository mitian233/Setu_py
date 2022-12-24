from flask import Flask,abort,send_file
import io,requests,json,logging
logging.basicConfig(level=logging.INFO)

ua = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54'}

app = Flask(__name__)

@app.route("/")
def index():
    json_data = {'status': 'ok'}
    return json_data

@app.route("/ranomdpic")
def getrandpic():
    try:
        random = requests.get('https://danbooru.donmai.us/posts/random.json', headers=ua)
        rc = random.content.decode()
        jsonfile = json.loads(rc)
        result = jsonfile['file_url']
    except Exception as e:
        logging.error(e)
        abort(500)
    except KeyError as e:
        logging.error(e)
        abort(500)
    else:
        logging.info('Successfully fetched random picture')
        if random.status_code == 200:
            try:
                pic = requests.get(result, headers=ua)
            except:
                abort(500)
            else:
                if pic.status_code == 200:
                    Buffer = io.BytesIO()
                    filename = result.split('/')[-1]
                    Buffer.write(pic.content)
                    Buffer.seek(0)
                    return send_file(Buffer, mimetype='image', attachment_filename=filename, as_attachment=False)
                else:
                    abort(pic.status_code)
        else:
            abort(random.status_code)