define([
    'backbone',
    'moment'
], function (Backbone) {

    const StatsSummary = Backbone.Model.extend({
        urlRoot: fbaProxyURL + '/api/hazard-event/',
        url: function () {
            return `${this.urlRoot}${this.id}/summary-stats/district/`
        }
    });

    return Backbone.Collection.extend({
        model: StatsSummary,
        urlRoot: fbaProxyURL + '/api/hazard-event/',
        url: function () {
            console.log(this.urlRoot)
            let urlString = `${this.urlRoot}${this.id}/`;
            if(this.parent_id && this.parent_level && this.admin_level){
                urlString = `${urlString}summary-stats/${this.parent_level}/${this.parent_id}/${this.admin_level}/`
                if(this.admin_id){
                    urlString = `${urlString}${this.admin_id}`
                }
            }
            else if(this.admin_level && this.admin_id){
                urlString = `${urlString}summary-stats/${this.admin_level}/${this.admin_id}`
            }
            else if(this.admin_level){
                urlString = `${urlString}summary-stats/${this.admin_level}/`
            }
            else {
                urlString = `${urlString}summary-stats/all`
            }
            return urlString;
        }
    });
});
