В рамках второго домашнего задания вам необходимо построить модифицированную модель распространения продукта по Бассу. Для реализации модели используется библиотека PySD, примеры использования которой были разобраны ранее.

Классическая модель Басса была реализована нами совместно на семинаре. Модификация модели заключена в следующем:

Добавить конкурирующую компанию (еще один контейнер), по аналогии с исходной (привлечение клиентов через прямую рекламу и «сарафанное радио»).
Клиенты после привлечения любой из компаний могут разочароваться и снова вернуться на рынок потенциальных клиентов (вероятность разочарования – новый параметр модели). Таким образом, имеется обратный поток клиентов в контейнер потенциальных клиентов.
Привлеченные клиенты одной компании могут напрямую воздействовать на клиентов конкурента, переманивая их в свою компанию (еще два новых параметра: уровень толерантности, т.е. восприимчивости, выраженный в форме вероятности перехода к конкуренту при контакте с его клиентами, а также уровень агрессивности привлечения, выраженный в форме вероятности прямой рекламы клиентам конкурента).
Комментарий. Очевидно, что при такой модификации все привлеченные клиенты у каждой из компаний делятся на три группы: довольные, нейтральные, недовольные. Первые осуществляют «сарафанное радио» и агрессивную рекламу, но сами не восприимчивы к агрессивной рекламе со стороны конкурента, а также не возвращаются в контейнер потенциальных клиентов. Вторые не осуществляют ни «сарафанное радио», ни агрессивную рекламу, сами при этом восприимчивы к агрессивной рекламе со стороны конкурента, но не возвращаются в контейнер потенциальных клиентов (то есть могут быть только переманены конкурентом и не помогают текущей компании). Третьи такие же, как и вторые, но могут вернуться в контейнер потенциальных клиентов.

Пункты задания:

Реализовать модифицированную модель Басса. (максимум 2 балла при правильной реализации)
Оценить сходимость модели, т.е. устойчивость пропорции распределения клиентов. (максимум 4 балла при правильной реализации)
Варьированием параметров модели (
p
11
,
p
13
,
p
21
,
p
23
), получить обучающую и проверочную выборки для построения ML модели. Общую численность людей, а также «человеческие» параметры такие, как частота контактов, восприимчивость, агрессивность остаются постоянными, варьируем только параметры, характеризующие компании, но не людей. Построить ML модель, предсказывающую предельную пропорцию распределения клиентов по начальным параметрам. Для полученной функции доли рынка выберите произвольную точку в образе и, анализируя обратную функцию при варьировании параметров 
p
11
 и 
p
13
, найдите в прообразе область соответствующую этой же доли рынка с максимальным отклонением 
±
 7%. Аналитическое построение обратной функции дает полный балл за этот пункт задания. (максимум 4 балла при правильной реализации)