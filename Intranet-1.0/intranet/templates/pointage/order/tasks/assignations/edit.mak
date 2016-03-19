<%namespace file="intranet.templates.pointage.order.tasks.assignations.widgets" import="assignation_section"/>
${assignation_section(actions="edit_or_delete",
                      title=title,
                      question=question,
                      error_message=error_message,
                      employee=employee,
                      task=task,
                      assignation=assignation,
                      form_errors=form_errors,
                      values=values,
                      **hidden)}
