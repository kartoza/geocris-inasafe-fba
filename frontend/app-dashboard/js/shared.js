var dispatcher;
var mapView;
var AppRequest;
var floodCollectionView;
var resetView = true;

String.prototype.replaceAll = function (search, replacement) {
    var target = this;
    return target.replace(new RegExp(search, 'g'), replacement);
};

String.prototype.capitalize = function () {
    var target = this;
    return target.charAt(0).toUpperCase() + target.slice(1);
};

function twoDigits(d) {
    if(0 <= d && d < 10) return "0" + d.toString();
    if(-10 < d && d < 0) return "-0" + (-1*d).toString();
    return d.toString();
}

Date.prototype.toMysqlFormat = function() {
    return this.getUTCFullYear() + "-" + twoDigits(1 + this.getUTCMonth()) + "-" + twoDigits(this.getUTCDate()) + " " + twoDigits(this.getUTCHours()) + ":" + twoDigits(this.getUTCMinutes()) + ":" + twoDigits(this.getUTCSeconds());
};

function toTitleCase(str) {
    return str.replace(/\w\S*/g, function(txt){
        return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
    });
}

const monthNames = ["January", "February", "March", "April", "May", "June",
  "July", "August", "September", "October", "November", "December"
];

/** Return xml filter format from data
 * the format is in xml
 * @param data = dictionary
 */
function toXmlAndFilter(data) {
    let filter = '<Filter>'
    if (Object.keys(data).length > 1) {
        filter += '<AND>'
    }
    Object.keys(data).forEach(function (key) {
        let value = data[key]
        filter += '' +
            '<PropertyIsEqualTo>' +
            '<PropertyName>' + key + '</PropertyName>' +
            '<Literal>' + value + '</Literal>' +
            '</PropertyIsEqualTo>'
    })
    if (Object.keys(data).length > 1) {
        filter += '</AND>'
    }
    filter += '</Filter>'
    return filter
}
