# RealEstate
Educational project: real estate price forecast

Ціль даного проекту - прогноз цін на вторинну нерухомість за заданими параметрами (кількість кімнат, район, площа і тд)

Встановлений інтерпретатор 3.10
В Корені проекту має бути файл data.csv, data_collector та microDistricts.json

Як працює проект:

1) запускаєм дата коллектор. Він збирає дані, але його можна перервати т.я. дані вже зібрані і поміщені в файл data.csv
  data_collector - скрипт збору (парсингу) даних. При запуску треба вказати будь-яке ім'я.

2) далі блок обробки даних, приведення до потрібного вигляду та включення додаткової метрики
   https://colab.research.google.com/drive/1f1Lwoss7C52XR8Qu5KRznAk3YZNXYk_L?usp=sharing

3) далі фінальний блок - випробування різних моделей, вибір найкращої та демонстрація прикладного значення проекту
   https://colab.research.google.com/drive/1o8eTM7U0B89ANrJ3WeO5dEWnkchxElLd?usp=sharing
