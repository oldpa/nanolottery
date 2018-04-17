import { Template } from 'meteor/templating';

import { Blocks } from '../api/blocks.js';

import './body.html';

Template.body.onCreated(function bodyOnCreated() {
  Meteor.subscribe('blocks');
});
Template.body.helpers({
    blocks() {
        return Blocks.find({});
    },
});
