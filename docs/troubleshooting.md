# Troubleshooting Guide

### Common questions:

??? Question "How can I use [...] with Stela?"
    The use cases in [Using Frameworks](frameworks.md) above give a good hint about how to use Stela with several python projects.
    If you have a question which this guideline didn't resolve, please open an
    [issue](https://github.com/megalus/stela/issues).

??? Question "Got Error: _Stela did not found value for <MY_VARIABLE>_, but MY_VARIABLE exists in .env file."
    Please check if the root project folder is the same as the stela configuration file. If is correct, and your
    .env file is in another folder, you can use the `env_path` parameter to set the path to the .env file. You can also
    turn on Stela logs (`export STELA_SHOW_LOGS=true`) to see if the .env file and stela configuration file are being
    loaded correctly.

### Example Apps

To see how this library works check the `Example Folder` provided [here](https://github.com/megalus/stela/tree/main/examples).

### Not working?

Don't panic. Get a towel and, please, open an [issue](https://github.com/megalus/stela/issues).
