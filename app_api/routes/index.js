var express = require('express');
var router = express.Router();
var ctrlr1 = require('../controllers/cntrlr1')

/* GET home page. */
router.get('/', ctrlr1.testPage);

module.exports = router;
