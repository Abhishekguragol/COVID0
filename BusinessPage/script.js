var status_check = {
    "yes": '<i class="fa fa-check"></i>',
    "no": '<i class="fa fa-close"></i>'
};

var businessInfo = [
    {
        title: "Marco's Kitchen",
        location: "Sector 23, Gurgaon",
        tags: ['Restaurant','Italian','Food'],
        safety_reviews: 110,
        stars: 3,
        government_regulations: [
            {
                title: "Sanitized kitchen",
                status: "verified"
            },
            {
                title: "Daily temperature checks",
                status: "yes"
            },
            {
                title: "Rider hand wash",
                status: "no"
            }
        ],
        added_safety: [
            {
                title: "Digital payment methods",
                status: "verified"
            },
            {
                title: "Seating and table distancing",
                status: "yes"
            },
            {
                title: "Daily temperature checks",
                status: "yes"
            },
            {
                title: "Rider hand wash",
                status: "no"
            }
        ],
        reviews: [
            {
                name: "Ruddhra Mysuru Raja",
                stars: 1,
                dated: "1 month ago",
                body: "Safety and all okay but no kaddlekai :(",
            },
            {
                name: "Rahul Suresh",
                stars: 4,
                dated: "2 months ago",
                body: "Good measures taken to ensure social distancing in restaurant premises. Contactless payment methods implemented!",
            }
        ]
    },
];

let businessObject = {};
const getObject = (name) => {
    for(var item in businessInfo) {
        if(businessInfo[item].title == name) {
            businessObject = businessInfo[item];
            break;
        }
    }
}

const getTags = () => {
    const genPill = (tagName) => {
        return '<span class="badge badge-info">'+tagName+'</span>';
    };

    var tag_list = '';
    businessObject.tags.forEach((tag) => {
        tag_list += genPill(tag);
    });

    return tag_list;
}

const getSafetyReviews = (name) => {
    return businessObject.safety_reviews;
}

const getReviewStars = (name) => {
    return stars = businessObject.stars;
}

const setReviewStars = (name) => {
    var stars = getReviewStars(name);
    var html_string = '';
    for(let i=0; i<stars; i++) html_string+='<i class="active fa fa-star"></i>';
    for(let i=0; i<(5-stars); i++) html_string+='<i class="fa fa-star"></i>';

    return html_string;
}

const setRuleTable = (name, container) => {
    var objArray = [];
    if(name == "government_regulations") objArray=businessObject.government_regulations;
    else if(name == "added_safety") objArray=businessObject.added_safety;

    var i = 0;
    objArray.forEach(item => {
        if(i < 3){
            var rule = '<td class="rule">'+item.title+'</td>';
            var adherence = '<td class="adherence">';
            var verified = '<td class="verified">';
        
            if(item.status == "verified") {
                verified += '<i><a href="#">Verified</a></i></td>'
                adherence += status_check["yes"] + '</td>';
            } else {
                adherence += status_check[item.status] + '</td>';
            }
        
            container.insertAdjacentHTML('beforeend', '<tr>'+adherence+rule+verified+'</tr>');
            i += 1;
        }
    });

    return (objArray.length - 3)
}

const getReviews = () => {
    var reviews = businessObject.reviews;
    var reviewString = '';
    for(var item in reviews) {
        var review = '';
        var review = '<div id="review"><p>';
        review += '<span id="reviewer_name">'+reviews[item].name+'</span>';

        var stars = reviews[item].stars;
        review += '<span id="review_rating">';
        for(let i=0; i<stars; i++) review+='<i class="active fa fa-star"></i>';
        for(let i=0; i<(5-stars); i++) review+='<i class="fa fa-star"></i>';
        review += '</span>';

        review += '<span id="review_dated">'+reviews[item].dated+'</span></p>';
        review += '<p>'+reviews[item].body+'</p></div>'

        reviewString += review;
    }

    return reviewString;
}

var business_name = document.getElementById("business_name");
var business_location = document.getElementById("business_location");
var business_tags = document.getElementById("business_tags");
var head_review_number = document.getElementById("head_review_number");
var head_review_stars = document.getElementById("head_review_stars");
var govReg = document.getElementById('govReg');
var more_govReg = document.getElementById('more_govReg');
var addSafe = document.getElementById('addSafe');
var more_addSafe = document.getElementById('more_addSafe');
var customer_reviews = document.getElementById('customer_reviews');

var name = "Marco's Kitchen";
getObject(name);

business_name.innerHTML = name;
business_location.innerHTML = businessObject.location;
business_tags.insertAdjacentHTML('beforeend', getTags());
head_review_number.insertAdjacentHTML('beforeend','<i>'+getSafetyReviews()+' Safety reviews<i>');
head_review_stars.insertAdjacentHTML('beforeend',setReviewStars());
var left1 = setRuleTable("government_regulations", govReg);
if(left1>0) more_govReg.insertAdjacentHTML('beforeend', '<br><p><a href="#">View all</a></p>');
var left2 = setRuleTable("added_safety", addSafe);
if(left2>0) more_addSafe.insertAdjacentHTML('beforeend', '<br><p><a href="#">View all</a></p>');

var review_string = getReviews();
customer_reviews.insertAdjacentHTML('beforeend', review_string);