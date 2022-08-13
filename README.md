# <img src="./static/ic_launcher-playstore.png" width="30"/> Random YouTube Video
this repo is the source code of [randomvideo.pythonanywhere.com](https://randomvideo.pythonanywhere.com/)
<br/>this website has been closed.
<br/>but there is a [Discord Bot](https://discord.com/api/oauth2/authorize?client_id=1005068511703470081&permissions=2048&scope=bot) instead.

### download virtualenv
```bash
pip3 install virtualenv
```
```bash
virtualenv venv
```
- **on windows:**
	```bash
	venv\Scripts\activate
	```
- **on linux:**
	```bash
	source venv/bin/activate
	```
### download requirements

```bash
pip3 install -r requirements.txt
```
### run server
```bash
python3 manage.py runserver
```
### api key
> create the **apikey.txt** file in the project directory and paste the youtube data api key there