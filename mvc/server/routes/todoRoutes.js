const express = require('express');
const Todo = require('../models/Todo');
const router = express.Router();

// @route POST /todos
// @desc Add a new todo
router.post('/todos', async (req, res) => {
  try {
    const newTodo = new Todo({
      text: req.body.text,
    });
    await newTodo.save();
    res.status(201).json(newTodo);
  } catch (err) {
    res.status(500).json({ message: 'Server error' });
  }
});

// @route GET /todos
// @desc Get all todos
router.get('/todos', async (req, res) => {
  try {
    const todos = await Todo.find();
    res.status(200).json(todos);
  } catch (err) {
    res.status(500).json({ message: 'Server error' });
  }
});

// @route PUT /todos/:id
// @desc Update todo completion status
router.put('/todos/:id', async (req, res) => {
  try {
    const updatedTodo = await Todo.findByIdAndUpdate(req.params.id, {
      completed: req.body.completed,
    }, { new: true });
    res.status(200).json(updatedTodo);
  } catch (err) {
    res.status(500).json({ message: 'Server error' });
  }
});

// @route DELETE /todos/:id
// @desc Delete todo
router.delete('/todos/:id', async (req, res) => {
  try {
    await Todo.findByIdAndDelete(req.params.id);
    res.status(200).json({ message: 'Todo deleted' });
  } catch (err) {
    res.status(500).json({ message: 'Server error' });
  }
});

module.exports = router;
