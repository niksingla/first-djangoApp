var title = document.title
document.title = "Entertainment"

var movie_count = 0;
var series_count = 0;
changesuggestion()
changetv()
function changesuggestion() {
  document.querySelector("#loader").hidden = false
  document.querySelector("#suggest").hidden = true
  document.querySelector("#noResult").hidden = true

  let genre = document.querySelector("#genre").value


  let fetch_url = "/apis/entertainment/?genre=" + genre

  fetch(fetch_url)
    .then(response => response.text())
    .then(data => {
      document.querySelector("#loader").hidden = true
      document.querySelector("#suggest").hidden = false
      data = JSON.parse(data)
      
      poster = data['poster']

      if ("request" in data) {

        document.querySelector("#suggest").hidden = true
        document.querySelector("#noResult").hidden = false
        document.querySelector("#noResult").innerHTML = `No suggestion this time <br><span class="text-muted">(Try again)</span>`
      }
      else {
        document.querySelector("#suggest > span > strong").innerHTML =
          `<a href="` + data['google_link'] + `" target="_blank" style="text-decoration: none; color: inherit;" >` + data['movie'] +
          `<span></span>
        <br><div class="m-auto p-2 "><img src="` + poster + `" alt="" width="180" height="258"></div></a> 
        
        <div id="information">
          <table class="mx-auto">
            <tbody>
              <tr>
                <td><strong>Genre</strong></td>
                <td>`+ data['genres'] + `</td>
              </tr>
              <tr>
                <td><strong>Release Date</strong></td>
                <td>`+ data['releaseDate'] + `</td>
              </tr>
              <tr>
                <td><strong>Runtime</strong></td>
                <td>`+ data['runtime'] + `</td>
              </tr>
            </tbody>
          </table>    
        </div>
        <br>
        <div class='buttons-suggest'>
        <button class="btn btn-outline-light btn-sm mt-1" type="button" onclick="shuffle();" id="shufficon">Other option</button>
        </div>`
        
      }
      if (genre == "") {
        var sug = document.querySelector("#suggest")
        var inside_sug = document.querySelector("#suggest > span")
        sug.innerHTML = "Top Suggestion - " + inside_sug.outerHTML
      }

      var imdb_link = "/apis/entertainment/?rating=" + data['movie'].replaceAll(' ', '+')

      fetch(imdb_link)
        .then(response => response.text())
        .then(data => {
          data = JSON.parse(data)
          var imdbFill = ""
          if(data['imdb'] !='' || data['rt']!=''){
            document.querySelector("#suggest > span > strong > a >span").innerHTML = `<br>`
          }
          if ('imdb' in data && data['imdb']!="")
            imdbFill += `<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACgAAAAoCAYAAACM/rhtAAAABmJLR0QA/wD/AP+gvaeTAAACZklEQVRYhe2WXUsUURyHn3NmnNkdzZcSQwVRUzeTroKSoJtuIugihD6FUAQFkURQF0JE0jcIhK76AF0lghBdlb2yrEnRixFamKszO+7M6UKdXW3WwdWaLua5On/mN2ee8zJnBhISEhISEnaD2GioNxjMGxmkMuIUwhcuzW5WDOACCDWBjjRHgYtAvHIlXBT3UYXrOtK4BlyJ22gLBoKrCGNRqElzFuiK2ygUwXsJdMbtURFFt07Zi1LOpQedPJ5uYn9dkae3XwU1wPGePOPDOc7fzfDuiwUQmpMSGq0iR9ptbgx9orOlwLk7/eTmUgBkx55HKQpZzcCyX9ce8HnBrJgxdJ9jXXl+5HWmsvu4+agjNDf7PcX8kl6xn6oEF1d0ct/SLDlaxUxdymd8OBfUM+uzVs7QvQxnR/s5fWuA6Y/W3gkCPHndEJkRZZvHD7l+YXABgEJRMpUN769qwYm39dXeGtBoeUHb91VoZseCLQ2rALz8YG2q/xY7Fuw44JI2fDy1tn59rfaeS5WzY0EpFN0HnaDOtDrbpHdPVXvw8LpUrenR1uRWzNluqXsRetpGU5Vg7/qy9rU6CBG+uX8u65wYORrUmZCt8HCquSQiw0dQ+YTchr62kuBWLFNRbxUBMDToaXQYaLcZPjO3KdffvkJdyqPW9NA0xcneX6HPEmrSDJ0C25WsFiUIqE8Xg1rTFCnDZ9nWMGp8pADHLeWiyDsavi8wanxSNWGn45+CBf6f/8CtFCSoyC92fKgXEiFHAC8y++/xEHJEAKiJ9CBSXQYOxSy1wQxSjIlT9rO4RRISEhISIvgNBk62x/TsAeYAAAAASUVORK5CYII="/>
              `+ data['imdb']
          if ('rt' in data && data['rt']!="")
            imdbFill += ` <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACgAAAAoCAYAAACM/rhtAAAABmJLR0QA/wD/AP+gvaeTAAAFW0lEQVRYhe2YaWxUVRTHf+dOO+0UECggFBOEFihqCyqLkCpFg+Be1GBcvpEYwWjEIFFiSJAY0KBRE0NSY4IBSQBDWKIiLiy1kLJUDFRkK7uytaXQlun0LccPM1Om8KbM0E7CB/9fbt67553ze/fce+67D/7XLaTS3fQu3U3vzvRpOsvRks1kqsNBdTi4ZDOZneW30wBDAXKBbCD7SiaDOsuvJGNcuoPZrjIJQAyqyr9GqFbYJUq2wvKI01dUqBMY7Sp5IvRXNxxLYOP0sXySaMy0ZAAVikSYGL0QQLW1L9ZuORq+J1Hbq0NxMZmYSaU4+wTPG2ECsAjlQMIPCvsUFqjhgbNjeDGZmEmlOCp9Y26hm2Zmnhxw+PFfx63KcYztaeezDROXjqoe8Fe/1cY1X8n2tdXJxkoKUF97d4R2zVqoPjP5ZM5Bs2X0akLpwXaf8TenUbzyfgbuzbFRXWF87nwp+/5wpwM6sz6YJT7zIZC5d+g2Kgo2goRnXkYwnewzt3EmtxaAfsd6UdfvMi0BK/JmMHZ9AYVleQBB0Dm+8vVfJBL3hotEp67yac6+1fhMCcDeIdupKPwJAH8onYKyXAq35vHP4AutgAVbc+l/pA/7JhyhavxRLL9NRUkVAhSU5QVAPncenDLclN/7qjDP7RCgO/DgMhF/SfT6wMCdiAr5O+5k9IZhZDZmANDlUqD1mS6XAmQE0xm14S7uKc9l55P7OTzyFAfGnaAgPIqATnMf2tPC78y4aUDn9Tkfi/ASvbLhcgNaW8cTX47BFovuNV3a2F4LGFWgIYPiFfcxfNNg/KFrwinTnaKSat+2dXHrYtwyo3MW3C3dur5Ffh4yewZMKob9h+hS678ODiCrIYM+p3vQ53QPshoyruvveb5bG/BWCfN1/NNxd564I6jB5sVkZWbIlMfCVXbjFnA1njniClM+K47b344C6ppPgee8Oj1HUN9bOFj9/vGMHQnZPdEdf6BlFTcTPCEplOi4p+5IGNC9EpwmqMjIEWEHi79JGVyUwzK+Fzw7PG/6zKP07A79+8LpM3D0ZMrIbFVOh4Icb256NmFAFXKxbKipQ9dsSBkcwDkrxBXXQYWhXv2ei0R95jZpbEIXLUb3VKUMzkVpcsL7uKv09LLxHEHRyB6mQCiUIjywYqqCiHruKN4pRusBtKau3dLSUVmxTEqtl433CFoth/RcDVQfTw1ZREHXuRpT+NvLxnsOVlYtBS1KEVerGpzY70hZ52XjXWawvgNaUgEVVb1tYWvr9LGNk77Sm8VDUv7DRSIHoFTIVqXGvvr+PmTlkD0bLnjZxv1YMC1mNuI9cTsiJ1KY3cjoGahPN/534nLE65Cda2pV5W3aHtg6pJDrcioUpOXq6lXQ2YN2/Xg2aUCAtPK1y1B9v6NgLkqd3cLJtnAYkfn5lZu+bu/ZhM4kTtGUuYjOI4ljqhIuI02OzWXHxtGYogyuT/hoyO7fbvjyCR+arKJnHjYi3wL9vfobHZsGx8ZSxVYXR0E9ZocItT7MtCG7f1mfSNzkjp3jpma7aaGZqLwJ9Ijer7ctzlvtb4kGueQTKXXUWpRfuaUm0Zg3d3CfOLW7G7JeFpfJKvpIdXNTt9gUxqjRCOUG+TnNtpcM+nNLfbKxbgqwDeyECWnVjf5hItrXRfoBGPSsizl7ya05NKqy0upojFtayYygAF2BLCATyIi0PsKrO9oCuIAT0zYDoUh7BWgkwfqaCODtwEDCPyeT+l3XjizCv+GOAZ5bXFSJ1LXudC4cQHrEZ48bGSaaYgG6RZwGCKc2QDjNEglITGvFtEo4vUHCKQ4CdUADCaT5P3ErEy/gfuLWAAAAAElFTkSuQmCC"/>`
              + data['rt']

          document.querySelector("#suggest > span > strong > a >span").innerHTML += imdbFill

        }
        )
        .catch(error => console.log("Some error"))

    })
    .catch(error => {

      document.querySelector("#loader").hidden = true
      document.querySelector("#suggest").hidden = false
      document.querySelector("#suggest").innerHTML = "Something went wrong"
    })
}
function shuffle() {
  changesuggestion()
}
 
function navTv() {
  document.querySelector("#Movies").hidden = true
  document.querySelector("#TVshows").hidden = false

  document.getElementById("movie-select").className = "nav-link"
  document.getElementById("tv-select").className = "nav-link active"


}
function navMovie() {
  document.querySelector("#Movies").hidden = false
  document.querySelector("#TVshows").hidden = true

  document.getElementById("movie-select").className = "nav-link active"
  document.getElementById("tv-select").className = "nav-link"
}

function changetv() {

  try {
    document.querySelector("#suggestions-tv").hidden = true
  }
  catch { }

  try {
    document.querySelector("#loadertv").hidden = false
  }
  catch { }
  try {
    document.querySelector("#noResult-tv").hidden = true
  }
  catch { }
  var gen = document.querySelector("#genretv").value

  if (gen != "") {
    document.querySelector("#tv-shuffle-btn").hidden = true
  }

  var fetch_url = "/apis/entertainment/?genre=" + gen + "&tvshow="
  fetch(fetch_url)
    .then(response => response.text())
    .then(data => {
      data = JSON.parse(data)
      if ("show" in data) {
        document.querySelector("#suggestions-tv").hidden = false
        document.querySelector("#suggestions-tv > a").setAttribute('href', data["google_link"])
        document.querySelector("#suggestions-tv > a > p").innerHTML = `Top Suggestions - <span><strong>` + data["show"] + `</strong><br></span> <span id= "ratings"></span>`
        document.querySelector("#suggestions-tv > img").setAttribute('src', data["poster"])
        document.querySelector("#information-tv").innerHTML = `
      <table class="mx-auto">
          <tbody>
            <tr>
              <td><strong>Streaming On</strong></td>
              <td>`+ data['streamingOn'] + `</td>
            </tr>
            <tr>
              <td><strong>Genre</strong></td>
              <td>`+ data['genres'] + `</td>
            </tr>
            <tr>
              <td><strong>Premiere Date</strong></td>
              <td>`+ data['premDate'] + `</td>
            </tr>
          </tbody>
        </table>`

        document.querySelector("#tv-shuffle-btn").hidden = false
      }
      try {
        document.querySelector("#loadertv").hidden = true
      }
      catch {

      }
      var ur = "/apis/entertainment/?" + "&tvshow=" + "&rating=" + data['show'].replaceAll(" ", "+")

      fetch(ur)
        .then(response => response.text())
        .then(data => {
          data = JSON.parse(data)
          var ratingImdb = data['imdb']
          var ratingRt = data['rt']
          if ('imdb' in data && data['imdb'] != "") {
            document.querySelector("#ratings").innerHTML += `
            <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACgAAAAoCAYAAACM/rhtAAAABmJLR0QA/wD/AP+gvaeTAAACZklEQVRYhe2WXUsUURyHn3NmnNkdzZcSQwVRUzeTroKSoJtuIugihD6FUAQFkURQF0JE0jcIhK76AF0lghBdlb2yrEnRixFamKszO+7M6UKdXW3WwdWaLua5On/mN2ee8zJnBhISEhISEnaD2GioNxjMGxmkMuIUwhcuzW5WDOACCDWBjjRHgYtAvHIlXBT3UYXrOtK4BlyJ22gLBoKrCGNRqElzFuiK2ygUwXsJdMbtURFFt07Zi1LOpQedPJ5uYn9dkae3XwU1wPGePOPDOc7fzfDuiwUQmpMSGq0iR9ptbgx9orOlwLk7/eTmUgBkx55HKQpZzcCyX9ce8HnBrJgxdJ9jXXl+5HWmsvu4+agjNDf7PcX8kl6xn6oEF1d0ct/SLDlaxUxdymd8OBfUM+uzVs7QvQxnR/s5fWuA6Y/W3gkCPHndEJkRZZvHD7l+YXABgEJRMpUN769qwYm39dXeGtBoeUHb91VoZseCLQ2rALz8YG2q/xY7Fuw44JI2fDy1tn59rfaeS5WzY0EpFN0HnaDOtDrbpHdPVXvw8LpUrenR1uRWzNluqXsRetpGU5Vg7/qy9rU6CBG+uX8u65wYORrUmZCt8HCquSQiw0dQ+YTchr62kuBWLFNRbxUBMDToaXQYaLcZPjO3KdffvkJdyqPW9NA0xcneX6HPEmrSDJ0C25WsFiUIqE8Xg1rTFCnDZ9nWMGp8pADHLeWiyDsavi8wanxSNWGn45+CBf6f/8CtFCSoyC92fKgXEiFHAC8y++/xEHJEAKiJ9CBSXQYOxSy1wQxSjIlT9rO4RRISEhISIvgNBk62x/TsAeYAAAAASUVORK5CYII="/>
            <strong>`+ data['imdb'] + `</strong>`
          }
          if ('rt' in data && data['rt'] != "") {
            document.querySelector("#ratings").innerHTML += `
            <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACgAAAAoCAYAAACM/rhtAAAABmJLR0QA/wD/AP+gvaeTAAAFW0lEQVRYhe2YaWxUVRTHf+dOO+0UECggFBOEFihqCyqLkCpFg+Be1GBcvpEYwWjEIFFiSJAY0KBRE0NSY4IBSQBDWKIiLiy1kLJUDFRkK7uytaXQlun0LccPM1Om8KbM0E7CB/9fbt67553ze/fce+67D/7XLaTS3fQu3U3vzvRpOsvRks1kqsNBdTi4ZDOZneW30wBDAXKBbCD7SiaDOsuvJGNcuoPZrjIJQAyqyr9GqFbYJUq2wvKI01dUqBMY7Sp5IvRXNxxLYOP0sXySaMy0ZAAVikSYGL0QQLW1L9ZuORq+J1Hbq0NxMZmYSaU4+wTPG2ECsAjlQMIPCvsUFqjhgbNjeDGZmEmlOCp9Y26hm2Zmnhxw+PFfx63KcYztaeezDROXjqoe8Fe/1cY1X8n2tdXJxkoKUF97d4R2zVqoPjP5ZM5Bs2X0akLpwXaf8TenUbzyfgbuzbFRXWF87nwp+/5wpwM6sz6YJT7zIZC5d+g2Kgo2goRnXkYwnewzt3EmtxaAfsd6UdfvMi0BK/JmMHZ9AYVleQBB0Dm+8vVfJBL3hotEp67yac6+1fhMCcDeIdupKPwJAH8onYKyXAq35vHP4AutgAVbc+l/pA/7JhyhavxRLL9NRUkVAhSU5QVAPncenDLclN/7qjDP7RCgO/DgMhF/SfT6wMCdiAr5O+5k9IZhZDZmANDlUqD1mS6XAmQE0xm14S7uKc9l55P7OTzyFAfGnaAgPIqATnMf2tPC78y4aUDn9Tkfi/ASvbLhcgNaW8cTX47BFovuNV3a2F4LGFWgIYPiFfcxfNNg/KFrwinTnaKSat+2dXHrYtwyo3MW3C3dur5Ffh4yewZMKob9h+hS678ODiCrIYM+p3vQ53QPshoyruvveb5bG/BWCfN1/NNxd564I6jB5sVkZWbIlMfCVXbjFnA1njniClM+K47b344C6ppPgee8Oj1HUN9bOFj9/vGMHQnZPdEdf6BlFTcTPCEplOi4p+5IGNC9EpwmqMjIEWEHi79JGVyUwzK+Fzw7PG/6zKP07A79+8LpM3D0ZMrIbFVOh4Icb256NmFAFXKxbKipQ9dsSBkcwDkrxBXXQYWhXv2ei0R95jZpbEIXLUb3VKUMzkVpcsL7uKv09LLxHEHRyB6mQCiUIjywYqqCiHruKN4pRusBtKau3dLSUVmxTEqtl433CFoth/RcDVQfTw1ZREHXuRpT+NvLxnsOVlYtBS1KEVerGpzY70hZ52XjXWawvgNaUgEVVb1tYWvr9LGNk77Sm8VDUv7DRSIHoFTIVqXGvvr+PmTlkD0bLnjZxv1YMC1mNuI9cTsiJ1KY3cjoGahPN/534nLE65Cda2pV5W3aHtg6pJDrcioUpOXq6lXQ2YN2/Xg2aUCAtPK1y1B9v6NgLkqd3cLJtnAYkfn5lZu+bu/ZhM4kTtGUuYjOI4ljqhIuI02OzWXHxtGYogyuT/hoyO7fbvjyCR+arKJnHjYi3wL9vfobHZsGx8ZSxVYXR0E9ZocItT7MtCG7f1mfSNzkjp3jpma7aaGZqLwJ9Ijer7ctzlvtb4kGueQTKXXUWpRfuaUm0Zg3d3CfOLW7G7JeFpfJKvpIdXNTt9gUxqjRCOUG+TnNtpcM+nNLfbKxbgqwDeyECWnVjf5hItrXRfoBGPSsizl7ya05NKqy0upojFtayYygAF2BLCATyIi0PsKrO9oCuIAT0zYDoUh7BWgkwfqaCODtwEDCPyeT+l3XjizCv+GOAZ5bXFSJ1LXudC4cQHrEZ48bGSaaYgG6RZwGCKc2QDjNEglITGvFtEo4vUHCKQ4CdUADCaT5P3ErEy/gfuLWAAAAAElFTkSuQmCC"/>
            <strong>`+ data['rt'] + `</strong>`
          }
        }
        )
        .catch(err => {

        })
    }
    )
    .catch(error => {
      document.querySelector('#noResult-tv').hidden = false
      document.querySelector('#suggestions-tv').hidden = true
    })
}
function shuffletv() {
  document.querySelector("#tv-shuffle-btn").hidden = true
  changetv()
}
