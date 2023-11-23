# setup of views to navigate through the app
from flask import Flask, render_template, flash, redirect, request, jsonify, url_for
from app import app
# from app import db
# from .forms import IncomeForm, ExpensesForm, GoalForm
# from .models import Income, Expenses, Goal

# home page
@app.route('/')
def index():
    return "cheese app"