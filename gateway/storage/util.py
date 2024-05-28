import pika, json

import pika.spec

def upload(f, fs,channel, access):
    try:
        fid = fs.put(f)
    except Exception as err:
        return "Internel Server Error", 500
    
    message =  {
        "vedio_file": str(fid),
        "mp3_file": None,
        "user_name": access["username"],
    }

    try:
        channel.basic_publish(
            exchange="",
            routig_key="vedio",
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            )
        )
    except:
        fs.delete(fid)
        return "Internel Server Error", 500