def get_weather(city, preferance):

    # preferance -> str (1 or 2)
    # 1> °C, km/h, mb, mm, km
    # 2> °F, miles/h, in, miles

    import requests as r
    from json import loads

    l = loads(
        r.get(
            f"https://api.weatherapi.com/v1/current.json?key=d623f13f71d34995aab85043220901&q={city}/"
        ).text
    )

    try:
        l["current"]
    except:
        return False

    a = loads(
        r.get(
            f"https://api.weatherapi.com/v1/astronomy.json?key=d623f13f71d34995aab85043220901&q={city}/"
        ).text
    )
    c = preferance

    if c not in ["1", "2"]:
        exit("Invalid Choice !")

    d = {
        "1r": f"{l['current']['temp_c']}°C",
        "2r": f"{l['current']['temp_f']}°F",
        "1f": f"{l['current']['feelslike_c']}°C",
        "2f": f"{l['current']['feelslike_f']}°F",
        "1w": f"{l['current']['wind_kph']} km/h",
        "2w": f"{l['current']['wind_mph']} miles/h",
        "1pres": f"{l['current']['pressure_mb']} milibars",
        "2pres": f"{l['current']['pressure_in']} in",
        "1precip": f"{l['current']['precip_mm']} mm",
        "2precip": f"{l['current']['precip_in']} in",
        "1vis": f"{l['current']['vis_km']} km",
        "2vis": f"{l['current']['vis_miles']} miles",
        "1g": f"{l['current']['gust_kph']} km/h",
        "2g": f"{l['current']['gust_mph']} miles/h",
    }

    return_data = {}

    if l["location"]["name"] == l["location"]["region"]:
        return_data.update(
            {"place": f"{l['location']['name']}, {l['location']['country']}"}
        )
    else:
        return_data.update(
            {
                "place": f"{l['location']['name']}, {l['location']['region']}, {l['location']['country']}"
            }
        )

    return_data.update(
        {
            "Current Temperature": f"{d[str(c)+'r']}",
            "Condition": f"{l['current']['condition']['text']}",
            "Condition Icon": f"https:{l['current']['condition']['icon']}",
            "Feels Like": f"{d[c+'f']}",
            "Wind Speed": f"{d[c+'w']}",
            "Wind Degree": f"{l['current']['wind_degree']}°",
            "Wind Direction": f"{l['current']['wind_dir']}",
            "Pressure": f"{d[c+'pres']}",
            "Rainfall": f"{d[c+'precip']}",
            "Humidity": f"{l['current']['humidity']}",
            "Visibility": f"{d[c+'vis']}",
            "Gust": f"{d[c+'g']}",
            "UV Index": f"{l['current']['uv']}",
            "Sunrise": f"{a['astronomy']['astro']['sunrise']}",
            "Sunset": f"{a['astronomy']['astro']['sunset']}",
            "Moonrise": f"{a['astronomy']['astro']['moonrise']}",
            "Moonset": f"{a['astronomy']['astro']['moonset']}",
            "Moon phase": f"{a['astronomy']['astro']['moon_phase']}",
            "Moon Illumination": f"{a['astronomy']['astro']['moon_illumination']}",
        }
    )

    return return_data


if __name__ == "__main__":
    resp = get_weather(input("Enter city name:\n>>>>>\t"), "1")
    print(resp)
