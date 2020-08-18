const es = require("@elastic/elasticsearch");

const esClient = new es.Client({
    node: 'http://localhost:9200'
});

const post_search_index = function(req, res, next) {
    res.render('recipe_search');
}

const get_search_index = async function (req, res, next) {
    query = {
        query: {
            match: {
                ingredients: {
                    query: req.query.q
                }
            }
        }
    }

    results = [];

    async function sendResponse() {
        const {body} = await esClient.search({
            index: 'recipe_index',
            body: query
        })
        for (i = 0; i < body.hits.hits.length; i++) {
            results.push(body.hits.hits[i]._source)
            // console.log(body.hits.hits[i]._source.title)
        }
        //res.send(results);

        //res.redirect('/results')
        console.log(results)
        res.json(results);

    }
    sendResponse();
}

const get_results = function (req, res, next) {
    res.json(results);
}

module.exports = {
    get_search_index,
    post_search_index,
    get_results
}