**Requirements:**
1. Python 3.6.2 х64
2. ~10gb свободных на жёстком диске
3. SSD иначе нейронка будет очень долго работать

**Гайд как сделать, чтобы работало:**
1. Клонируем в нашу основную дерикторию `git clone https://github.com/ria-com/nomeroff-net.git`

2. Сохраняем в корень этой же директории все файлы из этого репозитория

3. Ставим в настройках IDE интерпритатор Питона 3.6.2! **С другими версиями Nomeroff-net не работает**

4. Далее нам нужно поставить все либы. Они находятся в файле requiremnts. PyCharm предложит их установить - тыкаем install requirements. Если другая IDE, то вот питон команда `pip install -r requirements.txt --no-index --find-links`

5. Запускаем REST API на Фласке: `python app.py`

6. Делаем запрос на /getCarPlate с GET параметром url. Например: http://127.0.0.1:5000/getCarPlate?url=https://www.autocar.co.uk/sites/autocar.co.uk/files/styles/gallery_slide/public/images/car-reviews/first-drives/legacy/1_32.jpg?itok=WbZoz69D

P.S. Если при запуске консоль питона пишет, что `no module found`, то pip просто не смог его почему-то поставить и это надо сделать вручную, учитывая версии, которые указаны в файлике requirements.txt. Иначе не будет работать