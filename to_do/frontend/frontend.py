import streamlit as st
import requests
from datetime import datetime
import os


API_URL = os.getenv("API_URL")

st.set_page_config(page_title="Task Manager", layout="wide")


if 'session' not in st.session_state:
    st.session_state.session = requests.Session()
if 'is_authenticated' not in st.session_state:
    st.session_state.is_authenticated = False
if 'user_info' not in st.session_state:
    st.session_state.user_info = None



def logout():
    try:
        st.session_state.session.post(f"{API_URL}/registration/logout/")
    except:
        pass
    st.session_state.is_authenticated = False
    st.session_state.user_info = None
    st.session_state.session = requests.Session()
    st.rerun()

def check_auth():
    if st.session_state.is_authenticated:
        try:
            resp = st.session_state.session.get(f"{API_URL}/tasks/")
            if resp.status_code == 401:
                logout()
                return False
            return True
        except:
            return False
    return False



def page_login():
    st.title("🔐 Вход в систему")
    
    tab1, tab2 = st.tabs(["Вход", "Регистрация"])
    
    with tab1:
        with st.form("login_form"):
            email = st.text_input("Email", placeholder="example@mail.com")
            password = st.text_input("Пароль", type="password")
            submit = st.form_submit_button("Войти", use_container_width=True)
            
            if submit:
                with st.spinner("Вход..."):
                    try:
                        
                        response = st.session_state.session.post(
                            f"{API_URL}/registration/login/",
                            json={"email": email, "password": password}
                        )
                        if response.status_code == 200:
                            st.session_state.is_authenticated = True
                            st.session_state.user_info = {"email": email}
                            st.success("Успешный вход!")
                            st.rerun()
                        else:
                            st.error(f"Ошибка: {response.json().get('detail', 'Неверные данные')}")
                    except Exception as e:
                        st.error(f"Ошибка соединения: {e}")

    with tab2:
        with st.form("register_form"):
            reg_username = st.text_input("Имя пользователя", placeholder="username")
            reg_email = st.text_input("Email", placeholder="example@mail.com")
            reg_password = st.text_input("Пароль", type="password", help="Минимум 4 символа")
            submit_reg = st.form_submit_button("Зарегистрироваться", use_container_width=True)
            
            if submit_reg:
                with st.spinner("Регистрация..."):
                    try:
                        
                        response = st.session_state.session.post(
                            f"{API_URL}/registration/register/",
                            json={"email": reg_email, "password": reg_password, "username": reg_username}
                        )
                        if response.status_code == 200:
                            st.success("Пользователь создан! Теперь войдите.")
                        else:
                            st.error(f"Ошибка: {response.text}")
                    except Exception as e:
                        st.error(f"Ошибка соединения: {e}")

def page_tasks():
    st.title("📋 Управление задачами")
    
    
    try:
        resp = st.session_state.session.get(f"{API_URL}/tasks/")
        if resp.status_code == 200:
            tasks = resp.json()
            
            tasks = sorted(tasks, key=lambda x: x.get('created_at', ''))
            
            
            total_tasks = len(tasks)
            completed_tasks = sum(1 for t in tasks if t.get('is_checked', False))
            active_tasks = total_tasks - completed_tasks
            
        else:
            tasks = []
            total_tasks = completed_tasks = active_tasks = 0
            st.warning("Не удалось загрузить задачи")
    except Exception as e:
        tasks = []
        total_tasks = completed_tasks = active_tasks = 0
        st.error(f"Ошибка соединения с API: {e}")

    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="📊 Всего задач", value=total_tasks)
    with col2:
        st.metric(label="✅ Выполненные", value=completed_tasks)
    with col3:
        st.metric(label="⏳ Активные", value=active_tasks)
    
    st.divider()

    
    if tasks:
        for task in tasks:
            
            status_color = "✅" if task.get('is_checked', False) else "⬜"
            status_label = "Выполнено" if task.get('is_checked', False) else "В работе"
            
            with st.expander(f"{status_color} {task.get('task_name', 'Без названия')} - {status_label}"):
                col_info, col_actions = st.columns([3, 1])
                
                with col_info:
                    st.write(f"**Описание:** {task.get('task_description', 'Нет описания') or 'Нет описания'}")
                    st.write(f"**ID:** {task.get('id')}")
                    st.write(f"**Создано:** {task.get('created_at', 'Неизвестно')}")
                    st.write(f"**Статус:** {status_label}")
                
                with col_actions:
                    
                    is_checked = st.checkbox("Выполнено", value=task.get('is_checked', False), key=f"chk_{task['id']}")
                    
                    if is_checked != task.get('is_checked', False):
                        try:
                            r = st.session_state.session.put(
                                f"{API_URL}/tasks/update/{task['id']}",
                                json={
                                    "task_name": task.get('task_name', ''),
                                    "task_description": task.get('task_description', ''),
                                    "is_checked": is_checked
                                }
                            )
                            if r.status_code == 200:
                                st.success("Статус обновлён")
                                st.rerun()
                            else:
                                st.error(r.text)
                        except Exception as e:
                            st.error(e)
                    
                    st.divider()
                    
                    
                    if st.button("🗑️ Удалить", key=f"del_{task['id']}", type="secondary"):
                        try:
                            r = st.session_state.session.delete(f"{API_URL}/tasks/delete/{task['id']}")
                            if r.status_code == 200:
                                st.success("Удалено")
                                st.rerun()
                            else:
                                st.error(r.text)
                        except Exception as e:
                            st.error(e)
    else:
        st.info("📭 Список задач пуст. Добавьте первую задачу ниже!")

    
    st.divider()
    st.subheader("➕ Добавить новую задачу")
    with st.form("add_task_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            t_name = st.text_input("Название задачи", placeholder="Что нужно сделать?")
        with col2:
            t_desc = st.text_area("Описание", placeholder="Детали задачи...", height=100)
        
        submit_task = st.form_submit_button("Создать задачу", use_container_width=True, type="primary")
        
        if submit_task:
            if not t_name:
                st.error("Название задачи обязательно")
            else:
                try:
                    payload = {
                        "task_name": t_name, 
                        "task_description": t_desc
                    }
                    r = st.session_state.session.post(f"{API_URL}/tasks/add/", json=payload)
                    if r.status_code == 200:
                        st.success("Задача добавлена")
                        st.rerun()
                    else:
                        st.error(f"Ошибка: {r.text}")
                except Exception as e:
                    st.error(e)

def page_users():
    st.title("👥 Пользователи")
    
    
    try:
        resp = st.session_state.session.get(f"{API_URL}/users/")
        users = resp.json() if resp.status_code == 200 else []
    except Exception as e:
        users = []
        st.error(f"Ошибка загрузки пользователей: {e}")

    if users:
        
        for user in users:
            with st.container(border=True):
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.markdown(f"### 👤 {user.get('username', 'User')}")
                    st.write(f"**ID:** {user.get('id')}")
                with col2:
                    st.write(f"📧 {user.get('email')}")
                    st.write(f"✅ Выполнено задач: **{user.get('completed_tasks', 0)}**")
                    st.write(f"📋 Активных задач: **{user.get('active_tasks', 0)}**")
    else:
        st.info("Пользователи не найдены")

    st.divider()
    st.subheader("➕ Добавить пользователя")
    with st.form("add_user_form", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            u_username = st.text_input("Имя пользователя", placeholder="username")
        with col2:
            u_email = st.text_input("Email", placeholder="example@mail.com")
        with col3:
            u_pass = st.text_input("Пароль", type="password", placeholder="****")
        
        submit_user = st.form_submit_button("Добавить", use_container_width=True)
        
        if submit_user:
            if not u_username or not u_email or not u_pass:
                st.error("Все поля обязательны")
            else:
                try:
                    
                    r = st.session_state.session.post(
                        f"{API_URL}/users/add/", 
                        json={"username": u_username, "email": u_email, "password": u_pass}
                    )
                    if r.status_code == 200:
                        st.success("Пользователь добавлен")
                        st.rerun()
                    else:
                        st.error(r.text)
                except Exception as e:
                    st.error(e)



def main():
    
    with st.sidebar:
        st.header("🧭 Навигация")
        if st.session_state.is_authenticated:
            st.write(f"👤 **{st.session_state.user_info.get('email', 'User')}**")
            st.divider()
            if st.button("🚪 Выйти", use_container_width=True):
                logout()
            
            st.divider()
            page = st.radio("Разделы", ["📋 Задачи", "👥 Пользователи"], index=0)
        else:
            page = "Вход"

    
    if not st.session_state.is_authenticated:
        page_login()
    else:
        
        if not check_auth():
            st.warning("⚠️ Сессия истекла. Пожалуйста, войдите снова.")
            logout()
            return

        if page == "📋 Задачи":
            page_tasks()
        elif page == "👥 Пользователи":
            page_users()

if __name__ == "__main__":
    main()