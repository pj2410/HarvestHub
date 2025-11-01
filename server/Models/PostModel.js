const mongoose = require("mongoose");

const PostSchema = mongoose.Schema({
    heading: {
        type: String,
        required: true,
    },
    content: {
        type: String,
        required: true,
    },
    creatorname: {
        type: String,
        required: true,
    },
    creatorId: {
        type: String,
        required: true,
    },
    createdAt: {
      type: Date,
      default: new Date(),
    }, 
})

// Add indexes for better query performance
PostSchema.index({ createdAt: -1 });
PostSchema.index({ creatorId: 1 });

module.exports = mongoose.model("posts", PostSchema);