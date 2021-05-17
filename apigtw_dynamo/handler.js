"use strict";

let AWS = require("aws-sdk");
let client = new AWS.DynamoDB.DocumentClient();
let params;
let tableName;

if (tableName === null) {
  tableName = process.env.TABLE_NAME;
}

exports.getMessages = async (event, context) => {
  console.debug("getMessage event:", event);

  let params = {
    TableName: tableName,
  };
  console.debug("PARAMS", params);

  return await new Promise((resolve, reject) => {
    client.scan(params, (err, data) => {
      if (err) {
        console.error(`getMessages ERROR=${err.stack}`);
        resolve({
          statusCode: 400,
          error: `Could not get messages: ${err.stack}`,
        });
      } else {
        console.info(`getMessages data=${JSON.stringify(data)}`);
        resolve({
          statusCode: 200,
          body: JSON.stringify(data),
        });
      }
    });
  });
};

exports.getMessage = async (event, context) => {
  console.debug("getMessage event:", event);
  params = {
    TableName: tableName,
    Key: {
      date: event.pathParameters.date,
      time: event.queryStringParameters.time,
    },
  };

  return await new Promise((resolve, reject) => {
    client.get(params, (err, data) => {
      if (err) {
        console.error(`getMessage ERROR=${err.stack}`);
        resolve({
          statusCode: 400,
          error: `Could not get messages: ${err.stack}`,
        });
      } else {
        console.info(`getMessage data=${JSON.stringify(data)}`);
        resolve({
          statusCode: 200,
          body: JSON.stringify(data),
        });
      }
    });
  });
};

exports.postMessage = async (event, context) => {
  console.debug("postMessage event:", event);
  let parsedBody = JSON.parse(event.body);
  params = {
    TableName: tableName,
    Item: parsedBody.Item,
  };
  console.debug(params);

  return await new Promise((resolve, reject) => {
    client.put(params, (err, data) => {
      if (err) {
        console.error(`postMessage ERROR=${err.stack}`);
        resolve({
          statusCode: 400,
          error: `Could not post message: ${err.stack}`,
        });
      } else {
        console.info(`postMessage data=${JSON.stringify(data)}`);
        resolve({
          statusCode: 201,
          body: JSON.stringify(data),
        });
      }
    });
  });
};

exports.putMessage = async (event, context) => {
  console.debug("putMessage event:", event);
  let parsedBody = JSON.parse(event.body);

  params = {
    TableName: tableName,
    Key: {
      date: event.pathParameters.date,
      time: event.queryStringParameters.time,
    },
    UpdateExpression: parsedBody.UpdateExpression,
    ExpressionAttributeValues: parsedBody.ExpressionAttributeValues,
  };

  return await new Promise((resolve, reject) => {
    client.update(params, (err, data) => {
      if (err) {
        console.error(`putMessage ERROR=${err.stack}`);
        resolve({
          statusCode: 400,
          error: `Could not update message: ${err.stack}`,
        });
      } else {
        console.info(`putMessage data=${JSON.stringify(data)}`);
        resolve({
          statusCode: 204,
          body: JSON.stringify(data),
        });
      }
    });
  });
};

exports.deleteMessage = async (event, context) => {
  console.debug("deleteMessage event:", event);

  params = {
    TableName: tableName,
    Key: {
      date: event.pathParameters.date,
      time: event.queryStringParameters.time,
    },
  };
  console.debug(params.Key);

  return await new Promise((resolve, reject) => {
    client.delete(params, (err, data) => {
      if (err) {
        console.error(`deleteMessage ERROR=${err.stack}`);
        resolve({
          statusCode: 400,
          error: `Could not delete messages: ${err.stack}`,
        });
      } else {
        console.info(`deleteMessage data=${JSON.stringify(data)}`);
        resolve({
          statusCode: 200,
          body: JSON.stringify(data),
        });
      }
    });
  });
};
