const weather = {
    "apiKey": "e5e1y5c15ChOLpvTbpak4FlvKroTXcuoak32-Rwr8hHTGizfpqwWkJ1_avfJ6M-5ESUVfPv70nqTovH5DSPgcqQsqW6fzVyPEeV7kmkwP2PV4TwPv5MN7pAUj9oMY3Yx", // should prob put this in another folder, can't remmber how to do this at the moment
    getIceCreamShop: function (city) {
        fetch(
            "https://api.yelp.com/v3/businesses/search?term=ice cream&location="
             + city
             + this.apiKey
        ).then((response)=> response.json())
        .then((data) => this.displayWeather(data));
    },
    displayWeather: function(data) {
        // watched tutorial for this part
        // goes into the dict containing weather info for city
        // and pulls info to display
        const { name } = data;
        const { description }= data.weather[0];
        const { temp, humidity, temp_min, temp_max } = data.main;
        // acutally displays info
        document.querySelector(".city").innerText = "Weather in " + name;
        document.querySelector(".description").innerText = description;
        document.querySelector(".temp").innerText = temp + "°F";
        document.querySelector(".humidity").innerText = "Humidity: " + humidity + "%";
        document.querySelector(".temp_min").innerText = "Min: " + temp_min + "°F";
        document.querySelector(".temp_max").innerText = "Max: " + temp_max + "°F";
        // if searching for location's weather, removes hidden visibility styling
        document.querySelector(".weather").classList.remove("loading");
        document.body.style.backgroundImage = "url(https://source.unsplash.com/1920x1080/?" + name + ")"
    },
    search: function () {
        this.getWeather(document.querySelector(".search-bar").value)
    }
};

// will run search when search icon is clicked
document.querySelector(".search button").addEventListener("click", function () {
    weather.search();
});

// will run search when enter key is hit
document.querySelector(".search-bar").addEventListener("keyup", function (event) {
    if (event.key == "Enter") {
        weather.search();
    }
});

// will show a default city when loading up the page
weather.getWeather("New York City");
