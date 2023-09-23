from random import randint

word_good = ["Интересно", "Прикольно", "Удивительно"]
def get_random_word(words):return words[randint(0, len(words)-1)]

var_volgorad = [
    ["excur/volgograd_Var_scenario/text_1.txt", "excur/volgograd_Var_scenario/photo_1.png", "excur/volgograd_Var_scenario/map_1.png", ["Черная", "Белая", "Красная"]],
    ["excur/volgograd_Var_scenario/text_2.txt", "excur/volgograd_Var_scenario/photo_2.png", "excur/volgograd_Var_scenario/map_2.png", get_random_word(word_good)],
    ["excur/volgograd_Var_scenario/text_3.txt", "excur/volgograd_Var_scenario/photo_3.png", "excur/volgograd_Var_scenario/map_3.png", ["Черная", "Белая", "Красная"]],
    ["excur/volgograd_Var_scenario/text_4.txt", "excur/volgograd_Var_scenario/photo_4.png", "excur/volgograd_Var_scenario/map_4.png", get_random_word(word_good)]
]

romantic_volgorad = [
    ["excur/volgograd_romantic_scenario/text_1.txt", "excur/volgograd_romantic_scenario/photo_1.png", "excur/volgograd_romantic_scenario/map_1.png", get_random_word(word_good)],
    ["excur/volgograd_romantic_scenario/text_2.txt", "excur/volgograd_romantic_scenario/photo_2.png", "excur/volgograd_romantic_scenario/map_2.png", get_random_word(word_good)],
    ["excur/volgograd_romantic_scenario/text_3.txt", "excur/volgograd_romantic_scenario/photo_3.png", "excur/volgograd_romantic_scenario/map_3.png", get_random_word(word_good)],
    ["excur/volgograd_romantic_scenario/text_4.txt", "excur/volgograd_romantic_scenario/photo_4.png", "excur/volgograd_romantic_scenario/map_4.png", get_random_word(word_good)]
]

interactiv_volgorad = [
    ["excur/volgograd_Test_interactiv_scenario/text_1.txt", "excur/volgograd_Test_interactiv_scenario/photo_1.png", "excur/volgograd_Test_interactiv_scenario/map_1.png", get_random_word(word_good)],
    ["excur/volgograd_Test_interactiv_scenario/text_2.txt", "excur/volgograd_Test_interactiv_scenario/photo_2.png", "excur/volgograd_Test_interactiv_scenario/map_2.png", get_random_word(word_good)],
    ["excur/volgograd_Test_interactiv_scenario/text_3.txt", "excur/volgograd_Test_interactiv_scenario/photo_3.png", "excur/volgograd_Test_interactiv_scenario/map_3.png", get_random_word(word_good)],
    ["excur/volgograd_Test_interactiv_scenario/text_4.txt", "excur/volgograd_Test_interactiv_scenario/photo_4.png", "excur/volgograd_Test_interactiv_scenario/map_4.png", get_random_word(word_good)]
]
excur_in_krim_beach = [
  ["excur/excur_in_krim_beach/text_0.txt",["excur/excur_in_krim_beach/photo_0.png"],"excur/excur_in_krim_beach/map_0.png","excur/excur_in_krim_beach/help_text_0.txt","excur/excur_in_krim_beach/help_movie_0.mp3","Начнем!"],
  ["excur/excur_in_krim_beach/text_1.txt",["excur/excur_in_krim_beach/photo_1.png","excur/excur_in_krim_beach/video_1.mp4"],"excur/excur_in_krim_beach/map_1.png","excur/excur_in_krim_beach/help_text_1.txt","excur/excur_in_krim_beach/help_movie_1.mp3",'Я на месте'],
  ["excur/excur_in_krim_beach/text_2.txt",["excur/excur_in_krim_beach/photo_2.png"],"excur/excur_in_krim_beach/map_2.png","excur/excur_in_krim_beach/help_text_2.txt","excur/excur_in_krim_beach/help_movie_2.mp3",["Свадьба Николая I и Александры Федоровны","Начало войны","открытие часовни Николая Чудотворца"]],
  ["excur/excur_in_krim_beach/text_3.txt",["excur/excur_in_krim_beach/photo_3.png"],"excur/excur_in_krim_beach/map_3.png","excur/excur_in_krim_beach/help_text_3.txt","excur/excur_in_krim_beach/help_movie_3.mp3",'Уже иду'],
  ["excur/excur_in_krim_beach/text_4.txt",["excur/excur_in_krim_beach/photo_4.png"],"excur/excur_in_krim_beach/map_4.png","excur/excur_in_krim_beach/help_text_4.txt","excur/excur_in_krim_beach/help_movie_4.mp3",'Я перешел'],
  ["excur/excur_in_krim_beach/text_5.txt",["excur/excur_in_krim_beach/photo_5.png"],"excur/excur_in_krim_beach/map_5.png","excur/excur_in_krim_beach/help_text_5.txt","excur/excur_in_krim_beach/help_movie_5.mp3",'Я прошел'],
  ["excur/excur_in_krim_beach/text_6.txt",["excur/excur_in_krim_beach/photo_6.png"],"excur/excur_in_krim_beach/map_6.png","excur/excur_in_krim_beach/help_text_6.txt","excur/excur_in_krim_beach/help_movie_6.mp3",["Горький","Пушкин","Есенин"]],
  ["excur/excur_in_krim_beach/text_7.txt",["excur/excur_in_krim_beach/photo_7.png"],"excur/excur_in_krim_beach/map_7.png","excur/excur_in_krim_beach/help_text_7.txt","excur/excur_in_krim_beach/help_movie_7.mp3",["5","2","6"]],
  ["excur/excur_in_krim_beach/text_8.txt",[],"excur/excur_in_krim_beach/map_8.png","excur/excur_in_krim_beach/help_text_8.txt","excur/excur_in_krim_beach/help_movie_8.mp3",["Рузвельт","Черчилль","Сталин"]],
  ["excur/excur_in_krim_beach/text_9.txt",["excur/excur_in_krim_beach/photo_9.png", "excur/excur_in_krim_beach/video_9.mp4"],"excur/excur_in_krim_beach/map_9.png","excur/excur_in_krim_beach/help_text_9.txt","excur/excur_in_krim_beach/help_movie_9.mp3",'Я у перекрестка'],
  ["excur/excur_in_krim_beach/text_10.txt",["excur/excur_in_krim_beach/photo_10.png"],"excur/excur_in_krim_beach/map_10.png","excur/excur_in_krim_beach/help_text_10.txt","excur/excur_in_krim_beach/help_movie_10.mp3",'Я дошел до моста'],
  ["excur/excur_in_krim_beach/text_11.txt",["excur/excur_in_krim_beach/video_11.mp4"],"excur/excur_in_krim_beach/map_11.png","excur/excur_in_krim_beach/help_text_11.txt","excur/excur_in_krim_beach/help_movie_11.mp3",'Я у Площади Ленина'],
  ["excur/excur_in_krim_beach/text_12.txt",[],"excur/excur_in_krim_beach/map_12.png","excur/excur_in_krim_beach/help_text_12.txt","excur/excur_in_krim_beach/help_movie_12.mp3",'Да, здорово'],
  ["excur/excur_in_krim_beach/text_13.txt",[],"excur/excur_in_krim_beach/map_13.png","excur/excur_in_krim_beach/help_text_13.txt","excur/excur_in_krim_beach/help_movie_13.mp3",'Продолжить'],
  ["excur/excur_in_krim_beach/text_14.txt",["excur/excur_in_krim_beach/photo_14.png","excur/excur_in_krim_beach/video_14.mp4"],"excur/excur_in_krim_beach/map_14.png","excur/excur_in_krim_beach/help_text_14.txt","excur/excur_in_krim_beach/help_movie_14.mp3",'Классно'],
  ["excur/excur_in_krim_beach/text_15.txt",["excur/excur_in_krim_beach/photo_15.png"],"excur/excur_in_krim_beach/map_15.png","excur/excur_in_krim_beach/help_text_15.txt","excur/excur_in_krim_beach/help_movie_15.mp3",["1886","1896","1996"]],
  ["excur/excur_in_krim_beach/text_16.txt",["excur/excur_in_krim_beach/photo_16.png"],"excur/excur_in_krim_beach/map_16.png","excur/excur_in_krim_beach/help_text_16.txt","excur/excur_in_krim_beach/help_movie_16.mp3",'Хорошо, Я учту'],
  ["excur/excur_in_krim_beach/text_17.txt",[],"excur/excur_in_krim_beach/map_17.png","excur/excur_in_krim_beach/help_text_17.txt","excur/excur_in_krim_beach/help_movie_17.mp3",'Иду'],
  ["excur/excur_in_krim_beach/text_18.txt",["excur/excur_in_krim_beach/photo_18.png"],"excur/excur_in_krim_beach/map_18.png","excur/excur_in_krim_beach/help_text_18.txt","excur/excur_in_krim_beach/help_movie_18.mp3",'Пошутить про аренду места'],
  ["excur/excur_in_krim_beach/text_19.txt",["excur/excur_in_krim_beach/photo_19.png"],"excur/excur_in_krim_beach/map_19.png","excur/excur_in_krim_beach/help_text_19.txt","excur/excur_in_krim_beach/help_movie_19.mp3",'Обязательно посетим'],
  ["excur/excur_in_krim_beach/text_20.txt",[],"excur/excur_in_krim_beach/map_20.png","excur/excur_in_krim_beach/help_text_20.txt","excur/excur_in_krim_beach/help_movie_20.mp3",["Отъезд Романовых из России","Построили корабль","Открыли пароходство в Ялте"]],
  ["excur/excur_in_krim_beach/text_21.txt",["excur/excur_in_krim_beach/photo_21.png"],"excur/excur_in_krim_beach/map_21.png","excur/excur_in_krim_beach/help_text_21.txt","excur/excur_in_krim_beach/help_movie_21.mp3",'Интересно...'],
  ["excur/excur_in_krim_beach/text_22.txt",[],"excur/excur_in_krim_beach/map_22.png","excur/excur_in_krim_beach/help_text_22.txt","excur/excur_in_krim_beach/help_movie_22.mp3",'Следую по маршруту'],
  ["excur/excur_in_krim_beach/text_23.txt",[],"excur/excur_in_krim_beach/map_23.png","excur/excur_in_krim_beach/help_text_23.txt","excur/excur_in_krim_beach/help_movie_23.mp3",["Здесь встречались Сергеев-Ценский и Горький","открыли гостиницу Мариино","Открыли набережную Ялты"]],
  ["excur/excur_in_krim_beach/text_24.txt",[],"excur/excur_in_krim_beach/map_24.png","excur/excur_in_krim_beach/help_text_24.txt","excur/excur_in_krim_beach/help_movie_24.mp3",'Интересненько'],
  ["excur/excur_in_krim_beach/text_25.txt",[],"excur/excur_in_krim_beach/map_25.png","excur/excur_in_krim_beach/help_text_25.txt","excur/excur_in_krim_beach/help_movie_25.mp3",'Обязательно ознакомлюсь'],
  ["excur/excur_in_krim_beach/text_26.txt",["excur/excur_in_krim_beach/audio_26.mp3"],"excur/excur_in_krim_beach/map_26.png","excur/excur_in_krim_beach/help_text_26.txt","excur/excur_in_krim_beach/help_movie_26.mp3",'Тоже прочту'],
  ["excur/excur_in_krim_beach/text_27.txt",[],"excur/excur_in_krim_beach/map_27.png","excur/excur_in_krim_beach/help_text_27.txt","excur/excur_in_krim_beach/help_movie_27.mp3",'Ух ты, немало...'],
  ["excur/excur_in_krim_beach/text_28.txt",[],"excur/excur_in_krim_beach/map_28.png","excur/excur_in_krim_beach/help_text_28.txt","excur/excur_in_krim_beach/help_movie_28.mp3",'Продвигаюсь далее'],
  ["excur/excur_in_krim_beach/text_29.txt",[],"excur/excur_in_krim_beach/map_29.png","excur/excur_in_krim_beach/help_text_29.txt","excur/excur_in_krim_beach/help_movie_29.mp3",'Продолжаем'],
  ["excur/excur_in_krim_beach/text_30.txt",["excur/excur_in_krim_beach/photo_30.png"],"excur/excur_in_krim_beach/map_30.png","excur/excur_in_krim_beach/help_text_30.txt","excur/excur_in_krim_beach/help_movie_30.mp3",'Я на месте'],
  ["excur/excur_in_krim_beach/text_31.txt",["excur/excur_in_krim_beach/photo_31.png"],"excur/excur_in_krim_beach/map_31.png","excur/excur_in_krim_beach/help_text_31.txt","excur/excur_in_krim_beach/help_movie_31.mp3",'Познавательно'],
  ["excur/excur_in_krim_beach/text_32.txt",[],"excur/excur_in_krim_beach/map_32.png","excur/excur_in_krim_beach/help_text_32.txt","excur/excur_in_krim_beach/help_movie_32.mp3",'О, опять он'],
  ["excur/excur_in_krim_beach/text_33.txt",[],"excur/excur_in_krim_beach/map_33.png","excur/excur_in_krim_beach/help_text_33.txt","excur/excur_in_krim_beach/help_movie_33.mp3",'Да тут красиво...'],
  ["excur/excur_in_krim_beach/text_34.txt",[],"excur/excur_in_krim_beach/map_34.png","excur/excur_in_krim_beach/help_text_34.txt","excur/excur_in_krim_beach/help_movie_34.mp3",'Было интересно, Пока!']
]
                      
excur = {
    "Военный Волгоград": var_volgorad,
    "Романтический Волгоград": romantic_volgorad,
    "Интерактивный Волгоград": interactiv_volgorad,
    'Набережная Ялты, еë секреты и тайны': excur_in_krim_beach,
}
