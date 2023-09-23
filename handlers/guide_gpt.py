from config import bot, db, ADMINS, OPENAI_TOKEN
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from txt_read.read_txt import read_txt_file
from KeyboardMarkup.KeyboardMarkup import cancel_gpt, start_gpt, back_for_menu, clear_reset_kb
import states.states as states
import openai
import json
import os

users = {}

# махинации с списком юзеров
if os.path.exists("users.json"):
    with open("users.json", "r", encoding='utf-8') as f:
        users = json.load(f)

openai.api_key = OPENAI_TOKEN

max_token_count = 1024

async def reset_handler(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    try:
        del users[f"dialog_{call.from_user.id}"]
    except KeyError:
        return await call.message.answer('<b>Ошибка: возможно Гид уже остановлен!</b>', reply_markup=start_gpt())
    return await call.message.answer('<b>Гид остановлен!\n\nМожете продолжить пользоваться ботом!</b>', reply_markup=back_for_menu())


async def start_gpt_handler(call: types.CallbackQuery, state: FSMContext):
    contents = await read_txt_file(['maintxt\\help.txt'])
    contents = contents[0]
    
    await states.User.dialog.set()

    await call.message.answer(contents, reply_markup=clear_reset_kb())

async def dialog_gpt_handler(msg: types.Message, state: FSMContext):
    if f'dialog_{msg.from_user.id}' in users.keys():
        try:
            role_gpt = await read_txt_file(['maintxt\\gptsystem.txt'])
            
            msgs = await msg.answer('Обрабатываю ответ...')  
            
            await bot.send_chat_action(chat_id=msg.from_user.id, action="typing")
            print(f"{users[f'dialog_{msg.from_user.id}']}\n")
            print(f"{msg.text}")
            print(f'id: {msg.from_user.id}')
            response = await openai.ChatCompletion.acreate(
                model='gpt-3.5-turbo',
                messages=[
                    {"role": "system", "content": f"{users[f'dialog_{msg.from_user.id}']}; В твоей памяти есть имя пользователя с которым ты общаешься {msg.chat.first_name} можешь использовать его иногда, но не часто!"},
                    {"role": "user", "content": f"\n{msg.text}"},
                ],
                temperature=0.6,
                frequency_penalty=0.2,
                max_tokens=max_token_count,
                presence_penalty=0.4,
            
            )
          
                 
        except openai.error.InvalidRequestError as e:
            message = ''
            if e.code == 'context_incomplete':
                message = "Ошибка: Не удалось завершить запрос. Длина контекста превышает допустимый лимит токенов."
            else:
                message = "Ошибка: Проблема во время взаимодействия с ботом. Попробуйте еще раз."
            await msg.answer(message)
        else:
            try:

                response_text = response.choices[0].message.content

                users[f"dialog_{msg.from_user.id}"] = ''
                users[f"dialog_{msg.from_user.id}"] += f"\n{role_gpt}{msg.text}\n{response_text}"
                
                response.clear()
                await msgs.delete()
                
                

                await msg.answer(response_text, parse_mode='HTML', reply_markup=cancel_gpt())
                

            except:
                message = "Ошибка: Проблема во время обработки сообщения ботом. Попробуйте еще раз."
                await msg.answer(message)
    else:
        try:
            role_gpt = await read_txt_file(['maintxt\\gptsystem.txt'])
            
            msgs = await msg.answer('Обрабатываю ответ...')  
            
            await bot.send_chat_action(chat_id=msg.from_user.id, action="typing")
            print(f"{msg.text}")
            print(f'id: {msg.from_user.id}')
            response = await openai.ChatCompletion.acreate(
                model='gpt-3.5-turbo',
                messages=[
                    {"role": "system", "content": f"{role_gpt}; В твоей памяти есть имя пользователя с которым ты общаешься {msg.chat.first_name} можешь использовать его иногда, но не часто!"},
                    {"role": "user", "content": f"\n{msg.text}"},
                ],
                temperature=0.6,
                frequency_penalty=0.2,
                max_tokens=max_token_count,
                presence_penalty=0.4,
            
            )
          
                 
        except openai.error.InvalidRequestError as e:
            message = ''
            if e.code == 'context_incomplete':
                message = "Ошибка: Не удалось завершить запрос. Длина контекста превышает допустимый лимит токенов."
            else:
                message = "Ошибка: Проблема во время взаимодействия с ботом. Попробуйте еще раз."
            await msg.answer(message)
        else:
            try:

                response_text = response.choices[0].message.content

                users[f"dialog_{msg.from_user.id}"] = ''
                users[f"dialog_{msg.from_user.id}"] += f"\n{role_gpt}{msg.text}\n{response_text}"
                
                response.clear()
                await msgs.delete()
                
                

                await msg.answer(response_text, parse_mode='HTML', reply_markup=cancel_gpt())
                

            except:
                message = "Ошибка: Проблема во время обработки сообщения ботом. Попробуйте еще раз."
                await msg.answer(message)
   

def register_handlers_guide_gpt(dp: Dispatcher):
    dp.register_callback_query_handler(start_gpt_handler, text='start_gpt')  
    dp.register_message_handler(dialog_gpt_handler, state=states.User.dialog)  
    dp.register_callback_query_handler(reset_handler,  text='cancel_gpt', chat_type=['private'], state="*") 