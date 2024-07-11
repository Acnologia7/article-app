const { TestEnvironment } = require("jest-environment-jsdom");
const { transform } = require("typescript");

module.exports = {
    preset: 'ts-jest',
    testEnvironment: 'jest-environment-jsdom',
    transform: {
        "^.+\\.(js|jsx|ts|tsx)$": "babel-jest",
    }
};
