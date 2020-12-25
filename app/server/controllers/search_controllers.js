const es = require("@elastic/elasticsearch");
const stemmer = require('stemmer');

const esClient = new es.Client({
    node: 'http://localhost:9200'
});

// transforms an array into a unique one
Array.prototype.unique = function() {
    var a = this.concat();
    for(var i=0; i<a.length; ++i) {
        for(var j=i+1; j<a.length; ++j) {
            if(a[i] === a[j])
                a.splice(j--, 1);
        }
    }

    return a;
};

// checks if field is null or undefined
function isValidField(field) {
    if(typeof field === 'undefined') {
        return false;
    } else if(field === null){
        return false;
    } else  {
        return true
    }
}

function getTagWords() {
    const results = arguments;
    console.log("GET_TAG_RESULTS");
    console.log(results);
    // list of tag words
    let tagWords = [];
    let stemTag = [];
    // tag info
    let tagInfo = [];
    let result;
    for (result of results) {
        const recipe_category = result.recipe_category;
        const recipe_cuisine = result.recipe_cuisine;
        const recipe_keywords = result.keywords;
        if (isValidField(recipe_category)) {
            if (typeof recipe_category === 'string' || recipe_category instanceof String) {
                if (!stemTag.includes(stemmer(recipe_category))) {
                    tagWords.push(recipe_category);
                    stemTag.push(stemmer(recipe_category));
                    tagInfo.push(tagUrl(recipe_category, result.url));
                }
            }
        }


        if (isValidField(recipe_cuisine)) {
            if (!stemTag.includes(stemmer(recipe_cuisine))) {
                tagWords.push(recipe_cuisine);
                stemTag.push(stemmer(recipe_cuisine));
                tagInfo.push(returnTag(recipe_category, result.url));
            } else {
                tagInfo.push(returnTag(recipe_category, result.url));
            }
        }

        if (isValidField(recipe_keywords)) {
            let words = recipe_keywords.split(/[ ,]+/);
            let word;
            for (word of words) {
                if (!stemTag.includes(stemmer(word))) {
                    tagWords.push(word);
                    stemTag.push(stemmer(word));
                    tagInfo.push(returnTag(word, result.url))
                } else {
                    tagInfo.push(returnTag(word, result.url))
                }
            }
        }

    }

    function returnTag(tag, url) {
        return {
            tag: tag,
            url: url
        }
    }

    return tagInfo;
}

// Function that takes in a list of tags and returns an object with the tag ---> List[url]
function tagUrl(tagInfo) {
    // helper function to search tagUrlList:
    function search(tag, myArray){
        for (var i=0; i < myArray.length; i++) {
            if (myArray[i].tag === tag) {
                return myArray[i];
            }
        }
    }
    let wordsOver = []
    let tag;
    let tagUrlList = [];
    for (tag of tagInfo) {
        if (!wordsOver.includes(tag.tag)) {
            let tagUrl = {
                tag: tag.tag,
                url_list: [tag.url]
            }
            tagUrlList.push(tagUrl);
            wordsOver.push(tag.tag);
        } else {
            let tagUrl = search(tag.tag, tagUrlList);
            // add it to the list if it is a new url:
            if (isValidField(tagUrl) && !tagUrl.url_list.includes(tag.url)) {
                tagUrl.url_list.push(tag.url)
            }
        }
    }

    return tagUrlList;

}

let cuisines =
    'Ainu Albanian Argentine Andhra Anglo-Indian Arab Armenian Assyrian Awadhi Azerbaijani Balochi Belarusian Bangladeshi \
Bengali Berber Brazilian British Buddhist Bulgarian Cajun Cantonese Caribbean Chechen Chinese cuisine Chinese Islamic Circassian Crimean \
Tatar Cypriot Danish English Ethiopian Eritrean Estonian French Filipino Georgian German Goan Goan Catholic Greek Gujarati Hyderabad Indian cuisine \
Indian Chinese Indian Singaporean cuisine Indonesian Inuit Irish Italian-American Italian cuisine Jamaican Japanese Jewish Karnataka Kazakh Keralite \
Korean Kurdish Laotian Lebanese Latvian Lithuanian Louisiana Creole Maharashtrian Mangalorean Malay Malaysian Chinese cuisine Malaysian Indian cuisine \
Mediterranean cuisine Mennonite Mexican Mordovian Mughal Native American Nepalese New Mexican Odia Parsi Pashtun Polish Pennsylvania Dutch \
Pakistani Peranakan Persian Peruvian Portuguese Punjabi Rajasthani Romanian Russian Serbian quick easy slow delicious fast exquisite romantic\
dinner breakfast lunch healthy quarantine low appetizer vegetarian vegan veganism meal dishes hungarian main-dish side-dish '

// this will store the stemmed tagwords elements

function getCuisineKeywords() {
    let cuisineKeywords = [cuisines];
    let word;
    for (word of cuisines.split(/[ ,]+/)) {
        cuisineKeywords.push(stemmer(word));
    }
    return cuisineKeywords;
}

const cuisineWords = getCuisineKeywords();

// This function returns a query object based on user's query:
function returnQueryObject(query) {
    let queryIngredients = [];
    let q;
    for (q of query.split(/[ ,]+/)) {
        queryIngredients.push(stemmer(q));
    }
    let mustWords = [];
    let ing;
    for (ing of queryIngredients) {
        if (cuisineWords.includes(ing)) {
            mustWords.push(ing);
        }
    }
    const parsedQuery = queryIngredients.filter(x => !cuisineWords.includes(x));
    console.log(parsedQuery.join(" "));

    const multi_match = {
        multi_match: {
            query: parsedQuery.join(" "),
            type: "most_fields",
            fields: ["ingredients^3", "title", "description^2"]
        }
    }

    let queryObj;
    if (mustWords.length > 0) {
        const must_match = {
            match: {
                "recipeCuisine": {
                    query: query
                }
            }
        }

        const should_match = {
            match: {
                "keywords": {
                    query: query
                }
            },
            match: {
                "recipeCategory": {
                    query: query
                }
            }
        }

        queryObj = {
            query: {
                bool : {
                    must : must_match,
                    should: should_match
                }
            }
        }
    }
     else {
        const should_match = {
            match: {
                "keywords": {
                    query: query
                }
            },
            match: {
                "recipeCategory": {
                    query: query
                }
            },
            match: {
                "recipeCuisine": {
                    query: query
                }
            }
        }

        queryObj = {
            query : {
                bool: {
                    must: {
                        bool:{
                            should:[
                                multi_match,
                                should_match
                            ]
                        }
                    }
                }
            }
        }

    }


     return {
         query: queryObj,
         queryIngredients: parsedQuery
     }
}


const get_search_index = async function (req, res, next) {

    // the array of recipes that match the user's query
   let results = [];
   let queryObj = returnQueryObject(req.query.q);
    // this will store the stemmed query elements
    let queryIngredients = queryObj.queryIngredients;
    // console.log(req.query.q);
    console.log(queryObj.query);

    async function sendResponse() {
        const {body} = await esClient.search({
            index: 'recipe_index',
            body: queryObj.query
        })
        // console.log(body.hits.hits);
        for (i = 0; i < body.hits.hits.length; i++) {
            // console.log(body.hits.hits[i]);
            let source = body.hits.hits[i]._source;
            //define our score variable
            let score = body.hits.hits[i]._score;
            // log initial score
           // console.log(source.title + " " + score);


            // availIngredients stores the ingredients that match the user's query
            // unavailIngredients stortes the ingredients that don't match (and presumably means that
            // the user does not have those ingredients)
            let availIngredients = [];
            let unavailIngredients = [];

            // fill in availIngredients
            let q_ing;
            for (q_ing of queryIngredients){
                // this variable adds the appropriate amount to the score based on specific ingredient
                // matches to the query (for ex: if the query list is ['onions', 'tomato'], it
                // adds the appropriate score based on number of ingredients that onion and tomato respectively
                // i.e. a recipe that only has matches to onions will have a lower q_ing_score than a recipe
                // that matches to onions and tomatoes. Similarly, a recipe that has more ingredients that match to onions
                // when compared to one with less mathes to onion, the former recipe will recieve a higher score
                let q_ing_score = 0;
                let ing;
                for (ing of source.ingredients) {
                    let ing_stemmed = [];
                    let ing_token = ing.split(/[ ,]+/);
                    let t;
                    for (t of ing_token) {
                        ing_stemmed.push(stemmer(t));
                    }
                    // console.log(ing_stemmed);

                    // this boolean defines whether the q_ing is present or not:
                    let isQ = false;
                    let ing_stem;
                    for (ing_stem of ing_stemmed) {
                        if (ing_stem.localeCompare(q_ing) == 0) {
                           isQ = true;
                           break;
                        }
                    }
                    if (isQ) {
                        if (!availIngredients.includes(ing)) {
                            // if the ingredient matches and is not there in availIngredients,
                            // increment q_ing_score accordingly
                            q_ing_score++;
                            availIngredients.push(ing);

                        }
                    }
                 }
                 // add q_ing_score to the overall score variable. The ratio to total number of elements
                 // in the query array is added
                 score = score + (q_ing_score/queryIngredients.length * 5);
                }

            // fill in unavailIngredients
            unavailIngredients = source.ingredients.filter(x => !availIngredients.includes(x));
            // add the relevant proportion to the score :
            score = score + ((availIngredients.length/unavailIngredients.length) * 10);
            let result = {
                url: source.url,
                image_url: source.image_url,
                title: source.title,
                available_ingredients: availIngredients,
                unavailable_ingredients: unavailIngredients,
                steps: source.steps,
                score: score,
                rating: source.rating,
                nutrition_info: source.nutrition_info,
                author_name: source.author_name,
                keywords: source.keywords,
                recipe_category: source.recipe_category,
                recipe_cuisine: source.recipe_cuisine
            }
            console.log(result.title)
            results.push(result);



            // console.log(body.hits.hits[i]._source.title)
        }

        // sort the results by score:
        results.sort((a, b) => (a.score < b.score) ? 1 : -1)

        // test tagWords:
        console.log("LOG TAG");
        console.log(tagUrl(getTagWords.apply(null, results)));



        //res.redirect('/results')
        res.json(results);

    }

    // send the response and catch any error
    sendResponse().catch(err => console.log(err));
}

const get_results = function (req, res, next) {
    res.json(results);
}

const post_search_index = function (req, res, next) {

}

module.exports = {
    get_search_index,
    post_search_index,
    get_results
}