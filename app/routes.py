from flask import Blueprint, render_template, redirect, url_for, request, flash, send_from_directory, current_app, send_file
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from app.models import Note, Assignment, Todo, Attendance, User # Import models
from app import db
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('index.html')

@main.route('/dashboard')
@login_required
def dashboard():
    notes_count = Note.query.filter_by(user_id=current_user.id).count()
    assignments_pending = Assignment.query.filter_by(user_id=current_user.id, completed=False).count()
    overall_attendance = 0
    attendances = Attendance.query.filter_by(user_id=current_user.id).all()
    if attendances:
        total_p = sum([a.percentage for a in attendances])
        overall_attendance = round(total_p / len(attendances), 2)
    
    todos = Todo.query.filter_by(user_id=current_user.id, completed=False).order_by(Todo.priority.desc()).limit(5).all()

    return render_template('dashboard.html', notes_count=notes_count, assignments_pending=assignments_pending, overall_attendance=overall_attendance, todos=todos, all_attendance=attendances)

# --- Notes ---
@main.route('/notes', methods=['GET', 'POST'])
@login_required
def notes():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        file = request.files.get('file')
        filename = None

        if file and file.filename != '':
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

        new_note = Note(title=title, content=content, filename=filename, user_id=current_user.id)
        db.session.add(new_note)
        db.session.commit()
        flash('Note created!', 'success')
        return redirect(url_for('main.notes'))
    
    all_notes = Note.query.filter_by(user_id=current_user.id).order_by(Note.date_posted.desc()).all()
    return render_template('notes.html', notes=all_notes)

@main.route('/uploads/<filename>')
@login_required
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

@main.route('/notes/export/<int:id>')
@login_required
def export_note_pdf(id):
    note = Note.query.get_or_404(id)
    if note.user_id != current_user.id:
        flash('Permission denied.', 'danger')
        return redirect(url_for('main.notes'))

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    # Title
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, height - 50, note.title)
    
    # Date
    p.setFont("Helvetica", 10)
    p.drawString(50, height - 70, f"Date: {note.date_posted.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Content
    p.setFont("Helvetica", 12)
    text = p.beginText(50, height - 100)
    lines = note.content.split('\n')
    for line in lines:
        text.textLine(line)
    p.drawText(text)
    
    p.showPage()
    p.save()
    
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name=f"{note.title}.pdf", mimetype='application/pdf')

@main.route('/notes/delete/<int:id>')
@login_required
def delete_note(id):
    note = Note.query.get_or_404(id)
    if note.user_id == current_user.id:
        if note.filename:
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], note.filename)
            if os.path.exists(file_path):
                os.remove(file_path)
        db.session.delete(note)
        db.session.commit()
        flash('Note deleted.', 'info')
    return redirect(url_for('main.notes'))

# --- Assignments ---
@main.route('/assignments', methods=['GET', 'POST'])
@login_required
def assignments():
    if request.method == 'POST':
        subject = request.form.get('subject')
        title = request.form.get('title')
        description = request.form.get('description')
        deadline_str = request.form.get('deadline') # expects YYYY-MM-DD
        deadline = datetime.strptime(deadline_str, '%Y-%m-%d')

        new_assignment = Assignment(subject=subject, title=title, description=description, deadline=deadline, user_id=current_user.id)
        db.session.add(new_assignment)
        db.session.commit()
        flash('Assignment added!', 'success')
        return redirect(url_for('main.assignments'))

    all_assignments = Assignment.query.filter_by(user_id=current_user.id).order_by(Assignment.deadline).all()
    return render_template('assignments.html', assignments=all_assignments)

@main.route('/assignments/complete/<int:id>')
@login_required
def complete_assignment(id):
    assignment = Assignment.query.get_or_404(id)
    if assignment.user_id == current_user.id:
        assignment.completed = not assignment.completed
        db.session.commit()
    return redirect(url_for('main.assignments'))

@main.route('/assignments/delete/<int:id>')
@login_required
def delete_assignment(id):
    assignment = Assignment.query.get_or_404(id)
    if assignment.user_id == current_user.id:
        db.session.delete(assignment)
        db.session.commit()
    return redirect(url_for('main.assignments'))

# --- Attendance ---
@main.route('/attendance', methods=['GET', 'POST'])
@login_required
def attendance():
    if request.method == 'POST':
        subject = request.form.get('subject')
        total = int(request.form.get('total_classes', 0))
        attended = int(request.form.get('attended_classes', 0))
        
        att = Attendance(subject=subject, total_classes=total, attended_classes=attended, user_id=current_user.id)
        db.session.add(att)
        db.session.commit()
        flash('Subject added to attendance tracker.', 'success')
        return redirect(url_for('main.attendance'))

    all_attendance = Attendance.query.filter_by(user_id=current_user.id).all()
    return render_template('attendance.html', attendance=all_attendance)

@main.route('/attendance/update/<int:id>/<action>')
@login_required
def update_attendance(id, action):
    att = Attendance.query.get_or_404(id)
    if att.user_id == current_user.id:
        if action == 'present':
            att.attended_classes += 1
            att.total_classes += 1
        elif action == 'absent':
            att.total_classes += 1
        elif action == 'reset': # optional
            att.total_classes = 0
            att.attended_classes = 0
        db.session.commit()
    return redirect(url_for('main.attendance'))

@main.route('/attendance/delete/<int:id>')
@login_required
def delete_attendance(id):
    att = Attendance.query.get_or_404(id)
    if att.user_id == current_user.id:
        db.session.delete(att)
        db.session.commit()
    return redirect(url_for('main.attendance'))


# --- Todo ---
@main.route('/todo', methods=['GET', 'POST'])
@login_required
def todo():
    if request.method == 'POST':
        task = request.form.get('task')
        priority = request.form.get('priority')
        new_todo = Todo(task=task, priority=priority, user_id=current_user.id)
        db.session.add(new_todo)
        db.session.commit()
        return redirect(url_for('main.todo'))

    all_todos = Todo.query.filter_by(user_id=current_user.id).order_by(Todo.priority.desc()).all()
    return render_template('todo.html', todos=all_todos)

@main.route('/todo/complete/<int:id>')
@login_required
def complete_todo(id):
    todo = Todo.query.get_or_404(id)
    if todo.user_id == current_user.id:
        todo.completed = not todo.completed
        db.session.commit()
    return redirect(url_for('main.todo'))

@main.route('/todo/delete/<int:id>')
@login_required
def delete_todo(id):
    todo = Todo.query.get_or_404(id)
    if todo.user_id == current_user.id:
        db.session.delete(todo)
        db.session.commit()
    return redirect(url_for('main.todo'))
