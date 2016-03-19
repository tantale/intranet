<%namespace file="intranet.templates.pointage.order.tasks.assignations.widgets" import="assignation_section"/>
${assignation_section(actions="new",
                      title=title,
                      question=question,
                      error_message=error_message,
                      employee=employee,
                      task=task,
                      assignation=None,
                      form_errors=form_errors,
                      values=values,
                      **hidden)}
