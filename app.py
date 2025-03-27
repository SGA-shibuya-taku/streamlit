import streamlit as st
import requests
import pandas as pd
from setting import gmaps

if "pokemons" not in st.session_state:
    st.session_state.pokemons = {}
if "locs" not in st.session_state:
    st.session_state.locs = []


image_type = {
    "デフォルト": "image_url_official",
    "ゲーム（前）": "image_url_showdown_front",
    "ゲーム（後）": "image_url_showdown_back",
    "ポケモンホーム": "image_url_home",
}

language = {
    "日本語": "name",
    "英語": "name_en"
}


def get_pokemon(id):
    url = f"https://pokeapi.co/api/v2/pokemon/{id}"
    response = requests.get(url)
    data = response.json()
    pokemon = {}
    response_sp = requests.get(data["species"]["url"])
    pokemon["name"] = response_sp.json()["names"][0]["name"]
    pokemon["name_en"] = data["name"]
    pokemon[image_type["デフォルト"]] = data["sprites"]["other"]["official-artwork"]["front_default"]
    pokemon[image_type["ポケモンホーム"]] = data["sprites"]["other"]["home"]["front_default"]
    pokemon[image_type["ゲーム（前）"]] = data["sprites"]["other"]["showdown"]["front_default"]
    pokemon[image_type["ゲーム（後）"]] = data["sprites"]["other"]["showdown"]["back_default"]
    pokemon["cry_url"] = data["cries"]["latest"]
    pokemon["height"] = data["height"]

    st.session_state.pokemons[id] = pokemon


def get_location(query):
    loc = {}
    result = gmaps.geocode(query)
    loc["name"] = result[0]["address_components"][0]["short_name"]
    loc["lat"] = result[0]["geometry"]["location"]["lat"]
    loc["lon"] = result[0]["geometry"]["location"]["lng"]
    if loc not in st.session_state.locs:
        st.session_state.locs.append(loc)


num = st.sidebar.slider("横に表示する数を選択してください", 1, 10, 4)
current_image_type = st.sidebar.radio("表示する画像の種類を選んでください", list(image_type))
current_lang = st.sidebar.selectbox("言語", options=list(language))

tabs = st.tabs(["取得", "一覧", "その他"])


with tabs[0]:
    st.title("ポケモン取得")

    try:
        pokemon_id = st.text_input("図鑑番号を入力してください")
        if pokemon_id:
            get_pokemon(pokemon_id)
            pokemon = st.session_state.pokemons[pokemon_id]
            st.subheader(f"No.{pokemon_id} " + pokemon[language[current_lang]])
            st.image(pokemon[image_type[current_image_type]], use_container_width=True)
            cry_response = requests.get(pokemon["cry_url"])
            st.audio(cry_response.content, format="audio/ogg")
    except Exception as e:
        st.error(f"エラー: {e}")


with tabs[1]:
    st.title("取得したポケモン一覧")

    if st.button("リセット"):
        st.session_state.pokemons.clear()

    cols = st.columns(num)
    i = 0
    try:
        for id, pokemon in st.session_state.pokemons.items():
            cols[i % num].caption(f"{id}  " + pokemon[language[current_lang]])
            cols[i % num].image(pokemon[image_type[current_image_type]])
            i += 1
    except Exception as e:
        st.error(f"エラー: {e}")


with tabs[2]:
    query = st.text_input("場所を入力してください")
    if query:
        get_location(query)

    df = pd.DataFrame(st.session_state.locs)

    st.title("Map")
    st.table(df)
    st.map(df)
