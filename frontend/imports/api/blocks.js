import { Mongo } from 'meteor/mongo';

export const Blocks = new Mongo.Collection('blocks');

if (Meteor.isServer) {
  // This code only runs on the server
  Meteor.publish('blocks', function blocksPublication() {
    return Blocks.find();
  });
}
