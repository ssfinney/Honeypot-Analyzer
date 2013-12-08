class ApplicationController < ActionController::Base
  # Prevent CSRF attacks by raising an exception.
  # For APIs, you may want to use :null_session instead.
  protect_from_forgery with: :exception

  # This code throws a 404 when a routing error occurs
  # This still need to be implemented in the routes
  def page_not_found
    raise ActionController::RoutingError.new('Not Found')
  end

  # Redirect to /logs after successful user login
  def after_sign_in_path_for(resource)
    '/logs'
  end
end
