const BTN_DELETE_ACTION_NAME = "delete"
const DELETE_CHAR_URL = '/deleteChar'
const ADD_CHAR_URL = '/addChar'
const GET_CHARS_URL = '/getChars'

function addEventListeners() {
    let languageNames = ['greek', 'french']

    $(".btn-close").each(function (index) {
            if ($(this).attr('action') == BTN_DELETE_ACTION_NAME) {
                $(this).on('click', function (event) {
                    let data = {character: $(this).attr('character')}
                    fetch(makePostRequest(DELETE_CHAR_URL, data)).then(_ => {
                        generateCharacterBadges('greek')
                    })
                })
            }

        }
    )


    $("#greekAddCharButton").on('click', function (index) {
            let character = $("#greekAddCharInput").val()
            let data = {character: character}
            if (character) {
                fetch(makePostRequest(ADD_CHAR_URL, data)).then(_ => {
                    generateCharacterBadges('greek')
                })
            }

        }
    )
}

function makePostRequest(url, data) {
    return new Request(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
}

function makeGetRequest(url, params) {
    return url + '?' + Object.keys(params).map(key => key + '=' + params[key]).join('&');
}

function generateCharacterBadges(lang) {
    let url = makeGetRequest(GET_CHARS_URL, {language: lang})
    fetch(url).then(response => response.json())
        .then(data => {
            let elem = $("#" + lang + "Characters")
            elem.empty()
            let newHTML = ""
            let characters = data['characters']
            characters.forEach(c => {
                    newHTML += generateCharacterBadgeHTML(lang, c)
                }
            )
            elem.html(newHTML)
            addEventListeners()
        })

}

function generateCharacterBadgeHTML(lang, character) {
    return `<div id="${lang}Char${character}" class="badge bg-light text-dark"> 
                ${character}
                <button action="delete" character="${character}" type="button" class="btn-close"
                        aria-label="Close"></button>
            </div>`
}

generateCharacterBadges('greek')