var express = require('express');
var router = express.Router();
const searchController = require('../controllers/search_controllers');

/* GET home page. */
//router.post('/', searchController.post_search_index);
router.get('/', searchController.get_search_index);
router.get('/results', searchController.get_results)


module.exports = router;
