const express = require("express");
const mongoose = require("mongoose");
const cors = require("cors");

const app = express();
app.use(cors());
app.use(express.json());

mongoose.connect("mongodb://localhost:27017/studentDB", {
  useNewUrlParser: true,
  useUnifiedTopology: true
});


const StudentSchema = new mongoose.Schema({
  name: String,
  email: String,
  age: Number
});
const Student = mongoose.model("students", StudentSchema);



app.get("/students", async (req, res) => {
  const students = await Student.find();
  res.json(students);
});


app.post("/students", async (req, res) => {
  const student = new Student(req.body);
  await student.save();
  res.json(student);
});


app.put("/students/:id", async (req, res) => {
  const student = await Student.findByIdAndUpdate(req.params.id, req.body, { new: true });
  res.json(student);
});


app.delete("/students/:id", async (req, res) => {
  await Student.findByIdAndDelete(req.params.id);
  res.json({ message: "Deleted successfully" });
});

app.listen(3000, () => console.log("✅ Server running at http://localhost:3000"));
