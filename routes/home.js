module.exports.set = function(app){
    app.get('/', (req, res)=>{
        res.send('lmao')
    })
}