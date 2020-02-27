<%namespace file="intranet.templates.pointage.order.tasks.assignations.widgets" import="assignation_dialog"/>
${assignation_dialog(actions="new",
                     title=title,
                     question=question,
                     error_message=error_message,
                     employee=employee,
                     task=task,
                     assignation=None,
                     form_errors=form_errors,
                     values=values,
                     **hidden)}
